
from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Security
)
from pymysql import MySQLError

from app.models.schemas import EjecutarDemo
from app.services.demo_service import DemoService
from app.services.vehiculo_service import VehiculoService
from app.routers.estado import validar_api_key


router = APIRouter(
    prefix="/demos",
    tags=["DEMO"]
)

service = DemoService()
vehiculo_service = VehiculoService()


@router.get("/vehiculo/{id_vehiculo}")
def listar_demos(id_vehiculo: int = Path(gt=0)):
    vehiculo = vehiculo_service.obtener_vehiculo(id_vehiculo)

    if vehiculo is None:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    return service.obtener_demos(id_vehiculo)


@router.get("/{id_demo}/movimientos")
def consultar_movimientos_demo(
    id_demo: int = Path(gt=0)
):
    return service.obtener_movimientos_demo(id_demo)


@router.post(
    "/ejecutar",
    dependencies=[Security(validar_api_key)]
)
async def ejecutar_demo(datos: EjecutarDemo):
    try:
        return await service.iniciar_demo(
            datos.id_vehiculo,
            datos.id_demo
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except MySQLError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible consultar Amazon RDS"
        )


@router.post(
    "/cancelar/{id_vehiculo}",
    dependencies=[Security(validar_api_key)]
)
async def cancelar_demo(
    id_vehiculo: int = Path(gt=0)
):
    try:
        return await service.cancelar_demo(id_vehiculo)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get("/ejecucion/{id_vehiculo}")
def consultar_ejecucion(
    id_vehiculo: int = Path(gt=0)
):
    return service.consultar_ejecucion(id_vehiculo)
