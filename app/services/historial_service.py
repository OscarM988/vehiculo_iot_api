
from app.database.procedures import StoredProcedureRepository


class HistorialService:

    def __init__(self):
        self.repository = StoredProcedureRepository()

    def obtener_historial(self, id_vehiculo):
        registros = self.repository.ejecutar(
            "sp_obtener_historial",
            (id_vehiculo,)
        )

        # Mostrar únicamente movimientos individuales
        registros_individuales = [
            registro for registro in registros
            if registro.get("origen") != "DEMO"
        ]

        # Ordenar del más reciente al más antiguo
        registros_ordenados = sorted(
            registros_individuales,
            key=lambda r: (
                r["fecha_hora"],
                r["id_historial"]
            ),
            reverse=True
        )

        # Devolver un máximo de 10 movimientos
        return registros_ordenados[:10]
