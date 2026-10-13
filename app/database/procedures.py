
import re
from app.database.connection import DatabaseConnection


class StoredProcedureRepository:

    PROCEDIMIENTOS = {
        # VEHICULOS
        "sp_crear_vehiculo": 4,
        "sp_obtener_vehiculos": 0,
        "sp_obtener_vehiculo": 1,
        "sp_actualizar_vehiculo": 6,
        "sp_eliminar_vehiculo": 1,

        # COMANDOS
        "sp_crear_comando": 4,
        "sp_obtener_comandos_vehiculo": 1,
        "sp_actualizar_comando": 5,
        "sp_eliminar_comando": 1,

        # ESTADO
        "sp_actualizar_estado": 3,
        "sp_obtener_estado": 1,

        # HISTORIAL
        "sp_registrar_historial": 3,
        "sp_obtener_historial": 1,

        # DEMOS
        "sp_crear_demo": 3,
        "sp_obtener_demos": 1,
        "sp_actualizar_demo": 4,
        "sp_eliminar_demo": 1,

        # MOVIMIENTOS DE DEMO
        "sp_agregar_movimiento_demo": 5,
        "sp_obtener_movimientos_demo": 1,
        "sp_actualizar_movimiento_demo": 5,
        "sp_eliminar_movimiento_demo": 1,
    }

    def __init__(self):
        self.database = DatabaseConnection()

    def ejecutar(self, nombre, parametros=(), conexion=None):
        if nombre not in self.PROCEDIMIENTOS:
            raise ValueError("Procedimiento no permitido")

        parametros = tuple(parametros)

        if len(parametros) != self.PROCEDIMIENTOS[nombre]:
            raise ValueError(
                f"{nombre} requiere "
                f"{self.PROCEDIMIENTOS[nombre]} parámetros"
            )

        propia = conexion is None

        if propia:
            conexion = self.database.conectar()

        try:
            with conexion.cursor() as cursor:
                cursor.callproc(nombre, parametros)

                resultados = []

                while True:
                    if cursor.description is not None:
                        resultados.extend(cursor.fetchall())

                    if not cursor.nextset():
                        break

            if propia:
                conexion.commit()

            return resultados

        except Exception:
            if propia:
                conexion.rollback()
            raise

        finally:
            if propia:
                conexion.close()
