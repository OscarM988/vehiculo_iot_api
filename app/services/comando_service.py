
from app.database.procedures import StoredProcedureRepository


class ComandoService:

    def __init__(self):
        self.repository = StoredProcedureRepository()

    def obtener_comandos(self, id_vehiculo):
        return self.repository.ejecutar(
            "sp_obtener_comandos_vehiculo",
            (id_vehiculo,)
        )

    def crear_comando(
        self,
        id_vehiculo,
        nombre,
        codigo,
        descripcion
    ):
        return self.repository.ejecutar(
            "sp_crear_comando",
            (
                id_vehiculo,
                nombre,
                codigo,
                descripcion
            )
        )

    def actualizar_comando(
        self,
        id_comando,
        nombre,
        codigo,
        descripcion,
        activo
    ):
        return self.repository.ejecutar(
            "sp_actualizar_comando",
            (
                id_comando,
                nombre,
                codigo,
                descripcion,
                activo
            )
        )

    def eliminar_comando(self, id_comando):
        return self.repository.ejecutar(
            "sp_eliminar_comando",
            (id_comando,)
        )
