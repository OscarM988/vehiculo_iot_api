
from app.database.procedures import StoredProcedureRepository


class HistorialService:

    def __init__(self):
        self.repository = StoredProcedureRepository()

    def obtener_historial(self, id_vehiculo):
        registros = self.repository.ejecutar(
            "sp_obtener_historial",
            (id_vehiculo,)
        )

        registros_ordenados = sorted(
            registros,
            key=lambda r: (
                r["fecha_hora"],
                r["id_historial"]
            ),
            reverse=True
        )

        return registros_ordenados[:10]
