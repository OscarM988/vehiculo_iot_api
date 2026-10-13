
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
# MODELOS PARA MOVIMIENTOS DE DEMOS
# ---------------------------------------------

class AgregarMovimientoDemo(BaseModel):
    id_demo: int = Field(gt=0)
    id_comando: int = Field(gt=0)
    orden: int = Field(gt=0)
    duracion_ms: int = Field(gt=0)
    pausa_ms: int = Field(ge=0)


class ActualizarMovimientoDemo(BaseModel):
    id_comando: int = Field(gt=0)
    orden: int = Field(gt=0)
    duracion_ms: int = Field(gt=0)
    pausa_ms: int = Field(ge=0)


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
# AGREGAR MOVIMIENTO A UN DEMO
# ---------------------------------------------

@router.post(
    "/movimientos",
    dependencies=[Security(validar_api_key)]
)
def agregar_movimiento_demo(datos: AgregarMovimientoDemo):
    try:
        return service.agregar_movimiento_demo(
            datos.id_demo,
            datos.id_comando,
            datos.orden,
            datos.duracion_ms,
            datos.pausa_ms
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except MySQLError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible agregar el movimiento en Amazon RDS"
        )


# ---------------------------------------------
# ACTUALIZAR MOVIMIENTO DE UN DEMO
# ---------------------------------------------

@router.put(
    "/movimientos/{id_demo_movimiento}",
    dependencies=[Security(validar_api_key)]
)
def actualizar_movimiento_demo(
    datos: ActualizarMovimientoDemo,
    id_demo_movimiento: int = Path(gt=0)
):
    try:
        return service.actualizar_movimiento_demo(
            id_demo_movimiento,
            datos.id_comando,
            datos.orden,
            datos.duracion_ms,
            datos.pausa_ms
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except MySQLError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible actualizar el movimiento en Amazon RDS"
        )


# ---------------------------------------------
# ELIMINAR MOVIMIENTO DE UN DEMO
# ---------------------------------------------

@router.delete(
    "/movimientos/{id_demo_movimiento}",
    dependencies=[Security(validar_api_key)]
)
def eliminar_movimiento_demo(
    id_demo_movimiento: int = Path(gt=0)
):
    try:
        return service.eliminar_movimiento_demo(
            id_demo_movimiento
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except MySQLError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible eliminar el movimiento de Amazon RDS"
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
