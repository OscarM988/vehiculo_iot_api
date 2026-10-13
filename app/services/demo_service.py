
import asyncio
import logging

from app.database.procedures import StoredProcedureRepository
from app.services.estado_service import EstadoService
from app.services.vehiculo_service import VehiculoService
from app.services.websocket_manager import websocket_manager

logger = logging.getLogger(__name__)


class DemoService:

    def __init__(self):
        self.repository = StoredProcedureRepository()
        self.estado_service = EstadoService()
        self.vehiculo_service = VehiculoService()

        self.tareas = {}
        self.cancelaciones = {}
        self.estados = {}
        self.bloqueo = asyncio.Lock()

    # ---------------------------------------------
    # CONSULTAR DEMOS
    # ---------------------------------------------

    def obtener_demos(self, id_vehiculo):
        return self.repository.ejecutar(
            "sp_obtener_demos",
            (id_vehiculo,)
        )

    # ---------------------------------------------
    # CONSULTAR MOVIMIENTOS DE UN DEMO
    # ---------------------------------------------

    def obtener_movimientos_demo(self, id_demo):
        return self.repository.ejecutar(
            "sp_obtener_movimientos_demo",
            (id_demo,)
        )

    # ---------------------------------------------
    # CREAR DEMO
    # ---------------------------------------------

    def crear_demo(self, id_vehiculo, nombre, descripcion):
        vehiculo = self.vehiculo_service.obtener_vehiculo(
            id_vehiculo
        )

        if vehiculo is None:
            raise ValueError("Vehículo no encontrado")

        if not vehiculo["activo"]:
            raise ValueError("El vehículo está inactivo")

        return self.repository.ejecutar(
            "sp_crear_demo",
            (id_vehiculo, nombre, descripcion)
        )

    # ---------------------------------------------
    # ACTUALIZAR DEMO
    # ---------------------------------------------

    def actualizar_demo(
        self,
        id_demo,
        nombre,
        descripcion,
        activo
    ):
        return self.repository.ejecutar(
            "sp_actualizar_demo",
            (id_demo, nombre, descripcion, int(activo))
        )

    # ---------------------------------------------
    # ELIMINAR DEMO
    # ---------------------------------------------

    def eliminar_demo(self, id_demo):
        return self.repository.ejecutar(
            "sp_eliminar_demo",
            (id_demo,)
        )

    # ---------------------------------------------
    # VALIDAR DEMO ANTES DE EJECUTAR
    # ---------------------------------------------

    def validar_demo(self, id_vehiculo, id_demo):
        vehiculo = self.vehiculo_service.obtener_vehiculo(
            id_vehiculo
        )

        if vehiculo is None or not vehiculo["activo"]:
            raise ValueError(
                "Vehículo no existe o está inactivo"
            )

        demos = self.obtener_demos(id_vehiculo)

        demo = next(
            (d for d in demos if d["id_demo"] == id_demo),
            None
        )

        if demo is None or not demo["activo"]:
            raise ValueError(
                "DEMO no existe o está inactivo"
            )

        movimientos = self.obtener_movimientos_demo(
            id_demo
        )

        if not movimientos:
            raise ValueError(
                "El DEMO no tiene movimientos"
            )

        movimientos = sorted(
            movimientos,
            key=lambda m: m["orden"]
        )

        ordenes = set()

        for movimiento in movimientos:
            orden = movimiento["orden"]
            duracion = movimiento["duracion_ms"]
            pausa = movimiento["pausa_ms"]

            if orden in ordenes or orden <= 0:
                raise ValueError(
                    "Orden de movimiento inválido"
                )

            ordenes.add(orden)

            if duracion <= 0 or pausa < 0:
                raise ValueError(
                    "Duración o pausa inválida"
                )

            self.estado_service.validar_movimiento(
                id_vehiculo,
                movimiento["id_comando"]
            )

        return movimientos

    # ---------------------------------------------
    # NOTIFICACIONES WEBSOCKET
    # ---------------------------------------------

    async def notificar(
        self,
        tipo,
        id_vehiculo,
        **datos
    ):
        evento = websocket_manager.crear_evento(
            tipo,
            id_vehiculo,
            **datos
        )

        try:
            await websocket_manager.enviar_a_vehiculo(
                id_vehiculo,
                evento
            )

        except Exception:
            logger.exception(
                "Error enviando evento WebSocket"
            )

    # ---------------------------------------------
    # INICIAR DEMO
    # ---------------------------------------------

    async def iniciar_demo(
        self,
        id_vehiculo,
        id_demo
    ):
        async with self.bloqueo:

            if id_vehiculo in self.tareas:
                raise ValueError(
                    "Ya existe un DEMO ejecutándose "
                    "o finalizando para este vehículo"
                )

            movimientos = await asyncio.to_thread(
                self.validar_demo,
                id_vehiculo,
                id_demo
            )

            cancelacion = asyncio.Event()

            self.cancelaciones[id_vehiculo] = cancelacion
            self.estados[id_vehiculo] = "ejecutando"

            tarea = asyncio.create_task(
                self.ejecutar_demo(
                    id_vehiculo,
                    id_demo,
                    movimientos,
                    cancelacion
                )
            )

            self.tareas[id_vehiculo] = tarea

        return {
            "mensaje": "DEMO iniciado",
            "id_vehiculo": id_vehiculo,
            "id_demo": id_demo,
            "total_movimientos": len(movimientos),
            "estado": "ejecutando"
        }

    # ---------------------------------------------
    # ESPERAR DURACIÓN O PAUSA
    # ---------------------------------------------

    async def esperar(
        self,
        segundos,
        cancelacion
    ):
        try:
            await asyncio.wait_for(
                cancelacion.wait(),
                timeout=segundos
            )

        except asyncio.TimeoutError:
            pass

    # ---------------------------------------------
    # EJECUTAR MOVIMIENTOS DEL DEMO
    # ---------------------------------------------

    async def ejecutar_demo(
        self,
        id_vehiculo,
        id_demo,
        movimientos,
        cancelacion
    ):
        resultado_final = "finalizado"
        fallo_detener = False

        try:
            await self.notificar(
                "demo_iniciado",
                id_vehiculo,
                id_demo=id_demo
            )

            for movimiento in movimientos:

                if cancelacion.is_set():
                    resultado_final = "cancelado"
                    break

                # DEMO: actualiza estado sin historial
                resultado = await asyncio.to_thread(
                    self.estado_service.ejecutar_movimiento_demo,
                    id_vehiculo,
                    movimiento["id_comando"]
                )

                if cancelacion.is_set():
                    resultado_final = "cancelado"
                    break

                await self.notificar(
                    "demo_movimiento",
                    id_vehiculo,
                    id_demo=id_demo,
                    orden=movimiento["orden"],
                    duracion_ms=movimiento["duracion_ms"],
                    pausa_ms=movimiento["pausa_ms"],
                    movimiento=resultado
                )

                await self.esperar(
                    movimiento["duracion_ms"] / 1000,
                    cancelacion
                )

                if cancelacion.is_set():
                    resultado_final = "cancelado"
                    break

                await self.esperar(
                    movimiento["pausa_ms"] / 1000,
                    cancelacion
                )

            if cancelacion.is_set():
                resultado_final = "cancelado"

        except asyncio.CancelledError:
            resultado_final = "cancelado"
            raise

        except Exception:
            logger.exception(
                "Error durante la ejecución del DEMO"
            )

            resultado_final = "error"

        finally:

            if resultado_final != "finalizado":

                try:
                    # DETENER: actualiza solo el estado
                    await asyncio.to_thread(
                        self.estado_service.ejecutar_movimiento_demo,
                        id_vehiculo,
                        9
                    )

                except Exception:
                    fallo_detener = True

                    logger.exception(
                        "No se pudo actualizar "
                        "el estado a DETENER"
                    )

            self.estados[id_vehiculo] = resultado_final

            await self.notificar(
                "demo_" + resultado_final,
                id_vehiculo,
                id_demo=id_demo,
                estado=resultado_final,
                detener_registrado=(
                    not fallo_detener
                    if resultado_final != "finalizado"
                    else None
                )
            )

            async with self.bloqueo:

                tarea_actual = asyncio.current_task()

                if self.tareas.get(id_vehiculo) is tarea_actual:
                    self.cancelaciones.pop(
                        id_vehiculo,
                        None
                    )

                    self.tareas.pop(
                        id_vehiculo,
                        None
                    )

    # ---------------------------------------------
    # CANCELAR DEMO
    # ---------------------------------------------

    async def cancelar_demo(self, id_vehiculo):
        async with self.bloqueo:

            cancelacion = self.cancelaciones.get(
                id_vehiculo
            )

            if cancelacion is None:
                raise ValueError(
                    "No hay un DEMO en ejecución"
                )

            cancelacion.set()

            self.estados[id_vehiculo] = "cancelando"

        return {
            "mensaje": "Cancelación solicitada",
            "id_vehiculo": id_vehiculo,
            "estado": "cancelando"
        }

    # ---------------------------------------------
    # CONSULTAR ESTADO DE EJECUCIÓN
    # ---------------------------------------------

    def consultar_ejecucion(self, id_vehiculo):
        return {
            "id_vehiculo": id_vehiculo,
            "estado": self.estados.get(
                id_vehiculo,
                "sin_ejecucion"
            )
        }
