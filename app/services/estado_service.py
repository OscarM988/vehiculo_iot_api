
from app.database.procedures import StoredProcedureRepository
from app.services.vehiculo_service import VehiculoService
from app.services.comando_service import ComandoService


class EstadoService:

    def __init__(self):
        self.repository = StoredProcedureRepository()
        self.vehiculo_service = VehiculoService()
        self.comando_service = ComandoService()

    def obtener_estado(self, id_vehiculo):
        resultado = self.repository.ejecutar(
            "sp_obtener_estado",
            (id_vehiculo,)
        )

        if not resultado:
            return None

        return resultado[0]

    def validar_movimiento(self, id_vehiculo, id_comando):
        vehiculo = self.vehiculo_service.obtener_vehiculo(
            id_vehiculo
        )

        if vehiculo is None:
            raise ValueError("El vehículo no existe")

        if not vehiculo["activo"]:
            raise ValueError("El vehículo está inactivo")

        comandos = self.comando_service.obtener_comandos(
            id_vehiculo
        )

        comando = next(
            (
                c for c in comandos
                if c["id_comando"] == id_comando
            ),
            None
        )

        if comando is None:
            raise ValueError(
                "El comando no existe o no pertenece al vehículo"
            )

        if not comando["activo"]:
            raise ValueError("El comando está inactivo")

        return comando

    def actualizar_estado(
        self,
        id_vehiculo,
        id_comando,
        registrar_historial=False,
        origen="API"
    ):
        comando = self.validar_movimiento(
            id_vehiculo,
            id_comando
        )

        conexion = self.repository.database.conectar()

        try:
            # Conservar el valor conectado actual
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT conectado
                    FROM estado_vehiculo
                    WHERE id_vehiculo = %s
                    FOR UPDATE
                    """,
                    (id_vehiculo,)
                )
                fila = cursor.fetchone()

            conectado = (
                int(fila["conectado"])
                if fila is not None
                else 0
            )

            # Actualizar el último estado del vehículo
            self.repository.ejecutar(
                "sp_actualizar_estado",
                (id_vehiculo, id_comando, conectado),
                conexion=conexion
            )

            # Solo los movimientos individuales generan historial
            if registrar_historial:
                self.repository.ejecutar(
                    "sp_registrar_historial",
                    (id_vehiculo, id_comando, origen),
                    conexion=conexion
                )

            conexion.commit()

            return {
                "mensaje": (
                    "Movimiento individual registrado"
                    if registrar_historial
                    else "Estado DEMO actualizado"
                ),
                "id_vehiculo": id_vehiculo,
                "id_comando": id_comando,
                "comando": comando["nombre"],
                "codigo": comando["codigo"],
                "origen": origen,
                "persistido": True
            }

        except Exception:
            conexion.rollback()
            raise

        finally:
            conexion.close()

    def ejecutar_movimiento(
        self,
        id_vehiculo,
        id_comando,
        origen="API"
    ):
        # Movimiento individual: estado + historial
        return self.actualizar_estado(
            id_vehiculo,
            id_comando,
            registrar_historial=True,
            origen=origen
        )

    def ejecutar_movimiento_demo(
        self,
        id_vehiculo,
        id_comando
    ):
        # DEMO: solo estado, sin historial
        return self.actualizar_estado(
            id_vehiculo,
            id_comando,
            registrar_historial=False,
            origen="DEMO"
        )
