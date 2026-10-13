
from app.database.procedures import StoredProcedureRepository


class VehiculoService:

    def __init__(self):
        self.repository = StoredProcedureRepository()

    def obtener_vehiculos(self):
        return self.repository.ejecutar(
            "sp_obtener_vehiculos"
        )

    def obtener_vehiculo(self, id_vehiculo):
        resultado = self.repository.ejecutar(
            "sp_obtener_vehiculo",
            (id_vehiculo,)
        )

        if not resultado:
            return None

        return resultado[0]

    def crear_vehiculo(
        self,
        nombre,
        modelo,
        descripcion,
        microcontrolador
    ):
        return self.repository.ejecutar(
            "sp_crear_vehiculo",
            (
                nombre,
                modelo,
                descripcion,
                microcontrolador
            )
        )

    def actualizar_vehiculo(
        self,
        id_vehiculo,
        nombre,
        modelo,
        descripcion,
        microcontrolador,
        activo
    ):
        if self.obtener_vehiculo(id_vehiculo) is None:
            raise ValueError("Vehículo no encontrado")

        return self.repository.ejecutar(
            "sp_actualizar_vehiculo",
            (
                id_vehiculo,
                nombre,
                modelo,
                descripcion,
                microcontrolador,
                activo
            )
        )

    def eliminar_vehiculo(self, id_vehiculo):
        if self.obtener_vehiculo(id_vehiculo) is None:
            raise ValueError("Vehículo no encontrado")

        return self.repository.ejecutar(
            "sp_eliminar_vehiculo",
            (id_vehiculo,)
        )
