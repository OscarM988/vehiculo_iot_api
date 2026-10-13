
# API REST para Vehículo IoT

## Práctica 2.5 - APIs para IoT en entorno Dev

**Institución:** Tecnológico Nacional de México, campus Pachuca

**Carrera:** Ingeniería en Sistemas Computacionales

**Materia:** Implementación de Soluciones IoT

## Descripción

API REST desarrollada en Python con FastAPI y programación orientada a objetos para administrar vehículos IoT, comandos, estados, historial y DEMOS.

La aplicación se ejecuta localmente y utiliza Amazon RDS MySQL para almacenar información mediante 21 procedimientos almacenados.

También incorpora WebSocket para comunicar los movimientos individuales y la ejecución automática de DEMOS en tiempo real.

## Tecnologías utilizadas

- Python
- FastAPI
- Pydantic
- PyMySQL
- Amazon RDS MySQL
- WebSocket
- Uvicorn
- Visual Studio Code
- Thunder Client
- Git y GitHub

## Arquitectura del proyecto

```text
vehiculo_iot_api/
├── app/
│   ├── core/
│   ├── database/
│   │   ├── connection.py
│   │   └── procedures.py
│   ├── models/
│   │   └── schemas.py
│   ├── routers/
│   │   ├── vehiculos.py
│   │   ├── comandos.py
│   │   ├── estado.py
│   │   ├── historial.py
│   │   ├── demos.py
│   │   └── websocket.py
│   ├── services/
│   │   ├── vehiculo_service.py
│   │   ├── comando_service.py
│   │   ├── estado_service.py
│   │   ├── historial_service.py
│   │   ├── demo_service.py
│   │   └── websocket_manager.py
│   └── main.py
├── .env.example
├── .gitignore
├── probar_websocket.py
├── requirements.txt
└── README.md
```

### Componentes principales

- `core`: configuración de la aplicación.
- `database`: conexión a Amazon RDS y ejecución de procedimientos almacenados.
- `models`: modelos de validación con Pydantic.
- `routers`: endpoints HTTP y WebSocket.
- `services`: lógica de negocio mediante clases y servicios independientes.
- `main.py`: configuración principal de FastAPI.

## Instalación y ejecución local

### 1. Clonar el repositorio

```bash
git clone https://github.com/OscarM988/vehiculo_iot_api.git
cd vehiculo_iot_api
```

El repositorio es privado, por lo que se necesita autorización para clonarlo.

### 2. Crear el entorno virtual

```powershell
python -m venv .venv
```

Activarlo en Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Crear un archivo `.env` en la raíz del proyecto, tomando como referencia `.env.example`.

Variables requeridas:

```dotenv
DB_HOST=tu-instancia-rds.amazonaws.com
DB_PORT=3306
DB_NAME=vehiculo_iot
DB_USER=tu_usuario
DB_PASSWORD=tu_contrasena
API_KEY=tu_clave_api
```

Utilizar credenciales propias y una instancia Amazon RDS MySQL que contenga el esquema `vehiculo_iot` y sus 21 procedimientos almacenados.

**Nunca publicar `.env`, contraseñas ni API Keys.**

### 5. Ejecutar FastAPI

```powershell
uvicorn app.main:app --reload
```

La aplicación estará disponible en:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

## Endpoints principales

### Vehículos

| Método | Endpoint | Función |
|---|---|---|
| GET | `/vehiculos/` | Listar vehículos |
| GET | `/vehiculos/{id_vehiculo}` | Consultar vehículo |
| POST | `/vehiculos/` | Crear vehículo |
| PUT | `/vehiculos/{id_vehiculo}` | Actualizar vehículo |
| DELETE | `/vehiculos/{id_vehiculo}` | Eliminar vehículo |

### Comandos

| Método | Endpoint | Función |
|---|---|---|
| GET | `/comandos/vehiculo/{id_vehiculo}` | Consultar comandos |
| POST | `/comandos/` | Crear comando |
| PUT | `/comandos/{id_comando}` | Actualizar comando |
| DELETE | `/comandos/{id_comando}` | Eliminar comando |

### Estado e historial

| Método | Endpoint | Función |
|---|---|---|
| GET | `/estado/vehiculo/{id_vehiculo}` | Consultar estado |
| POST | `/estado/movimiento` | Registrar movimiento individual |
| GET | `/historial/vehiculo/{id_vehiculo}` | Consultar hasta 10 movimientos individuales recientes |

### DEMOS

| Método | Endpoint | Función |
|---|---|---|
| GET | `/demos/vehiculo/{id_vehiculo}` | Listar DEMOS |
| GET | `/demos/{id_demo}/movimientos` | Consultar movimientos |
| POST | `/demos` | Crear DEMO |
| PUT | `/demos/{id_demo}` | Actualizar DEMO |
| DELETE | `/demos/{id_demo}` | Eliminar DEMO |
| POST | `/demos/movimientos` | Agregar movimiento |
| PUT | `/demos/movimientos/{id_demo_movimiento}` | Actualizar movimiento |
| DELETE | `/demos/movimientos/{id_demo_movimiento}` | Eliminar movimiento |
| POST | `/demos/ejecutar` | Ejecutar DEMO |
| POST | `/demos/cancelar/{id_vehiculo}` | Cancelar DEMO |
| GET | `/demos/ejecucion/{id_vehiculo}` | Consultar ejecución |

Las operaciones de control y administración protegidas requieren el encabezado HTTP `X-API-Key`.

## Procedimientos almacenados

El proyecto integra los 21 procedimientos almacenados del esquema `vehiculo_iot`, distribuidos en las siguientes categorías:

- Vehículos: 5 procedimientos.
- Comandos: 4 procedimientos.
- Estado: 2 procedimientos.
- Historial: 2 procedimientos.
- DEMOS: 4 procedimientos.
- Movimientos de DEMOS: 4 procedimientos.

La ejecución se centraliza mediante `StoredProcedureRepository`.

## Comunicación WebSocket

### URL de conexión

```text
ws://localhost:8000/ws/vehiculo/1
```

El identificador final corresponde al vehículo que se desea monitorear.

### Eventos principales

- `estado_inicial`: estado recuperado al establecer la conexión.
- `demo_iniciado`: indica el inicio de una DEMO.
- `demo_movimiento`: notifica cada movimiento, incluyendo orden, duración y pausa.
- `demo_finalizado`: indica que la DEMO terminó correctamente.
- `demo_cancelado`: indica que se canceló la secuencia.
- `demo_error`: indica un error durante la ejecución.

Los mensajes se transmiten en formato JSON.

### Ejemplo de evento WebSocket

```json
{
  "tipo": "demo_movimiento",
  "id_vehiculo": 1,
  "id_demo": 1,
  "orden": 1,
  "duracion_ms": 2000,
  "pausa_ms": 400
}
```

El contenido real también puede incluir información del comando y una marca temporal.

## Ejecución de una DEMO

Endpoint:

```http
POST /demos/ejecutar
```

Ejemplo del cuerpo JSON:

```json
{
  "id_vehiculo": 1,
  "id_demo": 1
}
```

La API consulta los movimientos almacenados en Amazon RDS, los ejecuta lógicamente en orden y transmite los eventos mediante WebSocket.

Los movimientos individuales actualizan el estado y generan historial. Los movimientos ejecutados mediante DEMO actualizan el estado, pero no se agregan al historial.

## Pruebas funcionales

En la Práctica 2.5 se realizaron tres pruebas principales:

1. POST desde Thunder Client para registrar un movimiento individual y comprobar su persistencia.
2. GET desde Thunder Client para consultar un máximo de diez movimientos individuales recientes.
3. Ejecución de DEMO mediante POST desde Thunder Client y recepción de eventos WebSocket mediante un cliente en Google Chrome.

Durante la última prueba se ejecutaron ocho movimientos de la excavadora IoT. El historial mantuvo 44 registros antes y después de la DEMO.

## Seguridad y alcance

- El servidor FastAPI se ejecuta únicamente en localhost.
- La base de datos está alojada en Amazon RDS MySQL.
- Las credenciales se administran mediante variables de entorno.
- El archivo `.env` está excluido del repositorio.
- Las operaciones protegidas utilizan una API Key.
- La API no se encuentra desplegada públicamente.
- El despliegue mediante HTTPS y WSS corresponde a la Práctica 2.6.
```
