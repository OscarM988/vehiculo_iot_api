
from fastapi import APIRouter, HTTPException, Path
from app.services.historial_service import HistorialService
from app.services.vehiculo_service import VehiculoService

router = APIRouter(
    prefix="/historial",
    tags=["Historial"]
)

service = HistorialService()
vehiculo_service = VehiculoService()


@router.get("/vehiculo/{id_vehiculo}")
def consultar_historial(
    id_vehiculo: int = Path(gt=0)
):
    """
    Consulta los últimos 10 movimientos individuales.

    Stored Procedure: sp_obtener_historial.
    """

    vehiculo = vehiculo_service.obtener_vehiculo(id_vehiculo)

    if vehiculo is None:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    return service.obtener_historial(id_vehiculo)
