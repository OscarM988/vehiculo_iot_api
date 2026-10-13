
from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Security
)
from pydantic import BaseModel, Field
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


# ---------------------------------------------
# MODELOS PARA ADMINISTRAR DEMOS
# ---------------------------------------------

class CrearDemo(BaseModel):
    id_vehiculo: int = Field(gt=0)
    nombre: str = Field(min_length=1)
    descripcion: str = ""


class ActualizarDemo(BaseModel):
    nombre: str = Field(min_length=1)
    descripcion: str = ""
    activo: bool


# ---------------------------------------------
# CONSULTAR DEMOS DE UN VEHÍCULO
# ---------------------------------------------

@router.get("/vehiculo/{id_vehiculo}")
def listar_demos(id_vehiculo: int = Path(gt=0)):
    try:
        vehiculo = vehiculo_service.obtener_vehiculo(
            id_vehiculo
        )

        if vehiculo is None:
            raise HTTPException(
                status_code=404,
                detail="Vehículo no encontrado"
            )

        return service.obtener_demos(id_vehiculo)

    except MySQLError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible consultar Amazon RDS"
        )


# ---------------------------------------------
# CONSULTAR MOVIMIENTOS DE UN DEMO
# ---------------------------------------------

@router.get("/{id_demo}/movimientos")
def consultar_movimientos_demo(
    id_demo: int = Path(gt=0)
):
    try:
        return service.obtener_movimientos_demo(id_demo)

    except MySQLError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible consultar Amazon RDS"
        )


# ---------------------------------------------
# CREAR DEMO
# ---------------------------------------------

@router.post(
    "",
    dependencies=[Security(validar_api_key)]
)
def crear_demo(datos: CrearDemo):
    try:
        return service.crear_demo(
            datos.id_vehiculo,
            datos.nombre,
            datos.descripcion
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except MySQLError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible crear el DEMO en Amazon RDS"
        )


# ---------------------------------------------
# ACTUALIZAR DEMO
# ---------------------------------------------

@router.put(
    "/{id_demo}",
    dependencies=[Security(validar_api_key)]
)
def actualizar_demo(
    datos: ActualizarDemo,
    id_demo: int = Path(gt=0)
):
    try:
        return service.actualizar_demo(
            id_demo,
            datos.nombre,
            datos.descripcion,
            datos.activo
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except MySQLError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible actualizar el DEMO en Amazon RDS"
        )


# ---------------------------------------------
# ELIMINAR DEMO
# ---------------------------------------------

@router.delete(
    "/{id_demo}",
    dependencies=[Security(validar_api_key)]
)
def eliminar_demo(
    id_demo: int = Path(gt=0)
):
    try:
        return service.eliminar_demo(id_demo)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except MySQLError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible eliminar el DEMO de Amazon RDS"
        )


# ---------------------------------------------
# EJECUTAR DEMO
# ---------------------------------------------

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


# ---------------------------------------------
# CANCELAR DEMO
# ---------------------------------------------

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


# ---------------------------------------------
# CONSULTAR ESTADO DE EJECUCIÓN
# ---------------------------------------------

@router.get("/ejecucion/{id_vehiculo}")
def consultar_ejecucion(
    id_vehiculo: int = Path(gt=0)
):
    return service.consultar_ejecucion(id_vehiculo)
