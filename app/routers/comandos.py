
from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Security
)
from pymysql import MySQLError

from app.models.schemas import CrearComando, ActualizarComando
from app.services.comando_service import ComandoService
from app.services.vehiculo_service import VehiculoService
from app.routers.estado import validar_api_key


router = APIRouter(
    prefix="/comandos",
    tags=["Comandos"]
)

service = ComandoService()
vehiculo_service = VehiculoService()


@router.get("/vehiculo/{id_vehiculo}")
def listar_comandos(id_vehiculo: int = Path(gt=0)):
    """
    Consulta los comandos de un vehículo.
    SP: sp_obtener_comandos_vehiculo.
    """

    vehiculo = vehiculo_service.obtener_vehiculo(id_vehiculo)

    if vehiculo is None:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    return service.obtener_comandos(id_vehiculo)


@router.post("/", status_code=201)
def crear_comando(
    datos: CrearComando,
    api_key: str = Security(validar_api_key)
):
    """
    Crea un comando.
    SP: sp_crear_comando.
    """

    try:
        vehiculo = vehiculo_service.obtener_vehiculo(
            datos.id_vehiculo
        )

        if vehiculo is None:
            raise HTTPException(
                status_code=404,
                detail="Vehículo no encontrado"
            )

        resultado = service.crear_comando(
            datos.id_vehiculo,
            datos.nombre,
            datos.codigo,
            datos.descripcion
        )

        return {
            "mensaje": "Comando creado correctamente",
            "id_vehiculo": datos.id_vehiculo,
            "resultado": resultado
        }

    except MySQLError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible crear el comando en RDS"
        )


@router.put("/{id_comando}")
def actualizar_comando(
    datos: ActualizarComando,
    id_comando: int = Path(gt=0),
    api_key: str = Security(validar_api_key)
):
    """
    Actualiza un comando.
    SP: sp_actualizar_comando.
    """

    try:
        resultado = service.actualizar_comando(
            id_comando,
            datos.nombre,
            datos.codigo,
            datos.descripcion,
            int(datos.activo)
        )

        return {
            "mensaje": "Comando actualizado correctamente",
            "id_comando": id_comando,
            "resultado": resultado
        }

    except MySQLError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible actualizar el comando en RDS"
        )


@router.delete("/{id_comando}")
def eliminar_comando(
    id_comando: int = Path(gt=0),
    api_key: str = Security(validar_api_key)
):
    """
    Elimina un comando.
    SP: sp_eliminar_comando.
    """

    try:
        resultado = service.eliminar_comando(id_comando)

        return {
            "mensaje": "Comando eliminado correctamente",
            "id_comando": id_comando,
            "resultado": resultado
        }

    except MySQLError:
        raise HTTPException(
            status_code=503,
            detail="No fue posible eliminar el comando en RDS"
        )
