
import pymysql
from app.core.config import config


class DatabaseConnection:

    def __init__(self):
        self.host = config.DB_HOST
        self.port = config.DB_PORT
        self.user = config.DB_USER
        self.password = config.DB_PASSWORD
        self.database = config.DB_NAME

    def conectar(self):
        conexion = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            charset="utf8mb4",
            connect_timeout=10,
            cursorclass=pymysql.cursors.DictCursor
        )

        return conexion

    def probar_conexion(self):
        conexion = None

        try:
            conexion = self.conectar()

            with conexion.cursor() as cursor:
                cursor.execute("SELECT DATABASE() AS base_datos")
                resultado = cursor.fetchone()

            print("Conexión exitosa a Amazon RDS")
            print("Base de datos:", resultado["base_datos"])

            return True

        except pymysql.MySQLError as error:
            print("Error al conectar con Amazon RDS")
            print("Tipo de error:", type(error).__name__)
            return False

        finally:
            if conexion is not None:
                conexion.close()
