
import logging

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    status
)
from fastapi.encoders import jsonable_encoder
from fastapi.concurrency import run_in_threadpool

from app.services.websocket_manager import websocket_manager
from app.services.estado_service import EstadoService
from app.services.vehiculo_service import VehiculoService


router = APIRouter()

estado_service = EstadoService()
vehiculo_service = VehiculoService()

logger = logging.getLogger(__name__)


@router.websocket("/ws/vehiculo/{id_vehiculo}")
async def monitorear_vehiculo(
    websocket: WebSocket,
    id_vehiculo: int
):
    # Validar el identificador del vehículo
    if id_vehiculo <= 0:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION
        )
        return

    # Consultar el vehículo y su estado en Amazon RDS
    try:
        vehiculo = await run_in_threadpool(
            vehiculo_service.obtener_vehiculo,
            id_vehiculo
        )

        if vehiculo is None:
            await websocket.close(
                code=status.WS_1008_POLICY_VIOLATION
            )
            return

        estado = await run_in_threadpool(
            estado_service.obtener_estado,
            id_vehiculo
        )

    except Exception:
        logger.exception(
            "Error consultando RDS para vehículo %s",
            id_vehiculo
        )

        await websocket.close(
            code=status.WS_1011_INTERNAL_ERROR
        )
        return

    conectado = False

    try:
        # Aceptar conexión WebSocket
        await websocket_manager.conectar(
            websocket,
            id_vehiculo
        )
        conectado = True

        # Crear evento con el estado inicial
        evento = websocket_manager.crear_evento(
            "estado_inicial",
            id_vehiculo,
            estado=estado
        )

        # Convertir datetime y otros tipos a JSON
        evento_json = jsonable_encoder(evento)

        # Enviar estado inicial al cliente
        await websocket.send_json(evento_json)

        logger.info(
            "Estado inicial enviado al vehículo %s",
            id_vehiculo
        )

        # Mantener la conexión abierta
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        logger.info(
            "Cliente desconectado del vehículo %s",
            id_vehiculo
        )

    except Exception:
        logger.exception(
            "Error en WebSocket del vehículo %s",
            id_vehiculo
        )

        if conectado:
            try:
                await websocket.close(
                    code=status.WS_1011_INTERNAL_ERROR
                )
            except Exception:
                pass

    finally:
        # Eliminar la conexión del administrador
        websocket_manager.desconectar(
            websocket,
            id_vehiculo
        )
