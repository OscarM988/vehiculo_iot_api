
import os
import secrets
import logging

from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    status,
    Security
)
from fastapi.security import APIKeyHeader
from fastapi.encoders import jsonable_encoder
from fastapi.concurrency import run_in_threadpool
from dotenv import load_dotenv
from pymysql import MySQLError

from app.models.schemas import MovimientoIndividual
from app.services.estado_service import EstadoService
from app.services.vehiculo_service import VehiculoService
from app.services.websocket_manager import websocket_manager


load_dotenv()

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/estado",
    tags=["Estado"]
)

service = EstadoService()
vehiculo_service = VehiculoService()

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False
)


def validar_api_key(
    api_key: str | None = Security(api_key_header)
):
    clave_correcta = os.getenv("API_KEY")

    if not clave_correcta:
        raise HTTPException(
            status_code=503,
            detail="La clave de la API no está configurada"
        )

    if not api_key or not secrets.compare_digest(
        api_key,
        clave_correcta
    ):
        raise HTTPException(
            status_code=401,
            detail="Clave de API inválida o ausente"
        )


@router.get("/vehiculo/{id_vehiculo}")
def consultar_estado(
    id_vehiculo: int = Path(gt=0)
):
    """
    Consulta el último estado registrado.
    SP: sp_obtener_estado
    """

    vehiculo = vehiculo_service.obtener_vehiculo(
        id_vehiculo
    )

    if vehiculo is None:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    estado = service.obtener_estado(id_vehiculo)

    if estado is None:
        raise HTTPException(
            status_code=404,
            detail="El vehículo no tiene estado registrado"
        )

    return estado


@router.post(
    "/movimiento",
    status_code=status.HTTP_200_OK,
    dependencies=[Security(validar_api_key)]
)
async def registrar_movimiento(
    datos: MovimientoIndividual
):
    """
    Registra un movimiento individual.

    SP: sp_actualizar_estado
    SP: sp_registrar_historial

    Notifica por WebSocket después del commit.
    """

    try:
        resultado = await run_in_threadpool(
            service.ejecutar_movimiento,
            datos.id_vehiculo,
            datos.id_comando,
            datos.origen
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except MySQLError:
        logger.exception(
            "Error al registrar movimiento en RDS"
        )
        raise HTTPException(
            status_code=503,
            detail="No fue posible completar la operación en RDS"
        )

    # Consultar estado después del commit
    try:
        estado_actual = await run_in_threadpool(
            service.obtener_estado,
            datos.id_vehiculo
        )
    except Exception:
        logger.exception(
            "No se pudo consultar el estado actualizado"
        )
        estado_actual = None

    # Crear evento WebSocket
    evento = websocket_manager.crear_evento(
        "movimiento_individual",
        datos.id_vehiculo,
        movimiento=resultado,
        estado=estado_actual
    )

    # Convertir fechas y otros valores a JSON
    evento = jsonable_encoder(evento)

    # Notificar clientes conectados
    try:
        await websocket_manager.enviar_a_vehiculo(
            datos.id_vehiculo,
            evento
        )
    except Exception:
        logger.exception(
            "No se pudo enviar la notificación WebSocket"
        )

    return resultado
