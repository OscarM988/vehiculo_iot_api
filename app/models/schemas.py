
from pydantic import BaseModel, Field


# MOVIMIENTOS INDIVIDUALES
class MovimientoIndividual(BaseModel):
    id_vehiculo: int = Field(gt=0)
    id_comando: int = Field(gt=0)
    origen: str = Field(
        default="API",
        min_length=1,
        max_length=30
    )


# EJECUCION DE DEMOS
class EjecutarDemo(BaseModel):
    id_vehiculo: int = Field(gt=0)
    id_demo: int = Field(gt=0)


# CREAR VEHICULO
class CrearVehiculo(BaseModel):
    nombre: str = Field(min_length=1, max_length=80)
    modelo: str = Field(min_length=1, max_length=80)
    descripcion: str = Field(min_length=1, max_length=255)
    microcontrolador: str = Field(min_length=1, max_length=50)


# ACTUALIZAR VEHICULO
class ActualizarVehiculo(CrearVehiculo):
    activo: bool


# CREAR COMANDO
class CrearComando(BaseModel):
    id_vehiculo: int = Field(gt=0)
    nombre: str = Field(min_length=1, max_length=60)
    codigo: int = Field(ge=0)
    descripcion: str = Field(min_length=1, max_length=255)


# ACTUALIZAR COMANDO
class ActualizarComando(BaseModel):
    nombre: str = Field(min_length=1, max_length=60)
    codigo: int = Field(ge=0)
    descripcion: str = Field(min_length=1, max_length=255)
    activo: bool
