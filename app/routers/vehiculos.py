
from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Security
)
from pymysql import MySQLError

from app.models.schemas import CrearVehiculo, ActualizarVehiculo
from app.services.vehiculo_service import VehiculoService
from app.routers.estado import validar_api_key


router = APIRouter(
    prefix="/vehiculos",
    tags=["Vehículos"]
)

service = VehiculoService()


@router.get("/")
def listar_vehiculos():
    """Consulta vehículos mediante sp_obtener_vehiculos."""
    return service.obtener_vehiculos()


@router.get("/{id_vehiculo}")
def consultar_vehiculo(id_vehiculo: int = Path(gt=0)):
    """Consulta un vehículo mediante sp_obtener_vehiculo."""

    vehiculo = service.obtener_vehiculo(id_vehiculo)

    if vehiculo is None:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    return vehiculo


@router.post("/", status_code=201)
def crear_vehiculo(
    datos: CrearVehiculo,
    api_key: str = Security(validar_api_key)
):
    """Crea un vehículo mediante sp_crear_vehiculo."""

    try:
        resultado = service.crear_vehiculo(
            datos.nombre,
            datos.modelo,
            datos.descripcion,
            datos.microcontrolador
        )

        return {
            "mensaje": "Vehículo creado correctamente",
            "resultado": resultado
        }

    except MySQLError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible crear el vehículo en RDS"
        )


@router.put("/{id_vehiculo}")
def actualizar_vehiculo(
    datos: ActualizarVehiculo,
    id_vehiculo: int = Path(gt=0),
    api_key: str = Security(validar_api_key)
):
    """Actualiza un vehículo mediante sp_actualizar_vehiculo."""

    try:
        resultado = service.actualizar_vehiculo(
            id_vehiculo,
            datos.nombre,
            datos.modelo,
            datos.descripcion,
            datos.microcontrolador,
            int(datos.activo)
        )

        return {
            "mensaje": "Vehículo actualizado correctamente",
            "id_vehiculo": id_vehiculo,
            "resultado": resultado
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except MySQLError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible actualizar el vehículo en RDS"
        )


@router.delete("/{id_vehiculo}")
def eliminar_vehiculo(
    id_vehiculo: int = Path(gt=0),
    api_key: str = Security(validar_api_key)
):
    """Elimina un vehículo mediante sp_eliminar_vehiculo."""

    try:
        resultado = service.eliminar_vehiculo(id_vehiculo)

        return {
            "mensaje": "Vehículo eliminado correctamente",
            "id_vehiculo": id_vehiculo,
            "resultado": resultado
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except MySQLError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible eliminar el vehículo en RDS"
        )
