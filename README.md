# API REST para Vehículo IoT

## Práctica 2.5 y Examen Práctico 2.6 — Arquitectura y Tecnologías de IoT

**Institución:** Tecnológico Nacional de México, campus Pachuca  
**Carrera:** Ingeniería en Sistemas Computacionales  
**Materia:** Implementación de Soluciones IoT

---

## 1. Descripción

API REST desarrollada en **Python con FastAPI y Programación Orientada a Objetos (POO)** para administrar vehículos IoT, comandos, estados, historial de movimientos y DEMOS automatizadas.

El proyecto se desarrolló inicialmente en la Práctica 2.5 y posteriormente se migró a **Amazon EC2** como parte del Examen Práctico 2.6.

La aplicación utiliza **Amazon RDS for MySQL** para almacenar información mediante seis tablas y 21 procedimientos almacenados.

También incorpora WebSocket para transmitir movimientos individuales y ejecutar DEMOS en tiempo real.

Actualmente, la API está publicada mediante **HTTPS y WebSocket seguro (WSS)**, utilizando Duck DNS, Caddy y certificados TLS de Let's Encrypt.

La solución funciona desde clientes externos y permanece operativa aunque Visual Studio Code y el Escritorio Remoto estén cerrados.

---

## 2. Tecnologías utilizadas

### Desarrollo de software

- Python 3.14
- FastAPI
- Pydantic
- PyMySQL
- Uvicorn
- WebSocket
- Programación Orientada a Objetos
- Visual Studio Code
- Thunder Client
- Git y GitHub

### Infraestructura AWS

- Amazon EC2
- Windows Server 2025
- Amazon RDS for MySQL
- Grupos de seguridad de AWS
- IP elástica

### Publicación y seguridad

- Duck DNS
- Caddy Server
- Let's Encrypt
- HTTPS
- WebSocket seguro (WSS)
- API Key
- Variables de entorno
- Windows Task Scheduler

---

## 3. Arquitectura de la solución

El proyecto utiliza una arquitectura cliente-servidor que permite acceder públicamente a los servicios de FastAPI mediante conexiones seguras.

**Flujo de comunicación:**

Cliente externo (Thunder Client / Swagger UI / WebSocket)

↓

HTTPS / WSS

↓

Duck DNS — `vehiculo-iot.duckdns.org`

↓

Amazon EC2 — Windows Server 2025

↓

Caddy — Proxy inverso HTTPS/WSS

↓

FastAPI / Uvicorn — `127.0.0.1:8000`

↓

PyMySQL / Stored Procedures

↓

Amazon RDS MySQL — `vehiculo_iot`

### Funcionamiento

1. Un cliente externo realiza solicitudes HTTPS o establece conexiones WSS.
2. Duck DNS permite resolver el subdominio hacia la dirección pública de Amazon EC2.
3. Caddy administra la conexión TLS y redirige las solicitudes hacia FastAPI.
4. FastAPI procesa las operaciones mediante routers, servicios y modelos Pydantic.
5. PyMySQL ejecuta los procedimientos almacenados correspondientes.
6. Amazon RDS conserva la información de vehículos, comandos, estados, historial y DEMOS.
7. WebSocket comunica los eventos y movimientos a los clientes conectados.

---

## 4. Arquitectura del proyecto

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

**core:** Configuración general de la aplicación.

**database:** Conexión con Amazon RDS y ejecución de procedimientos almacenados.

**models:** Validación de entradas y respuestas mediante Pydantic.

**routers:** Definición de los endpoints HTTP y WebSocket.

**services:** Implementación de la lógica de negocio mediante clases y servicios independientes.

**main.py:** Configuración principal de FastAPI y registro de routers.

**StoredProcedureRepository:** Centraliza la ejecución de procedimientos almacenados.

**websocket_manager.py:** Administra las conexiones y notificaciones WebSocket.

---

## 5. Instalación y ejecución local

### 5.1. Clonar el repositorio

```bash
git clone https://github.com/OscarM988/vehiculo_iot_api.git
cd vehiculo_iot_api
```

El repositorio es privado, por lo que se necesita autorización para clonarlo.

### 5.2. Crear el entorno virtual

```powershell
python -m venv .venv
```

Activar en Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5.3. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 5.4. Configurar las variables de entorno

Crear un archivo `.env` en la carpeta principal del proyecto, tomando como referencia `.env.example`.

```dotenv
DB_HOST=tu-instancia-rds.amazonaws.com
DB_PORT=3306
DB_NAME=vehiculo_iot
DB_USER=tu_usuario
DB_PASSWORD=tu_contrasena
API_KEY=tu_clave_api
```

Las credenciales deben configurarse de manera privada.

**Nunca publicar el archivo `.env`, contraseñas, API Keys ni tokens de acceso.**

### 5.5. Ejecutar FastAPI localmente

```powershell
python -m uvicorn app.main:app --reload
```

Direcciones locales:

**API REST:** `http://127.0.0.1:8000`

**Swagger UI:** `http://127.0.0.1:8000/docs`

**WebSocket:** `ws://127.0.0.1:8000/ws/vehiculo/1`

---

## 6. Endpoints principales

### 6.1. Vehículos

| Método | Endpoint | Función |
|---|---|---|
| GET | `/vehiculos/` | Listar vehículos |
| GET | `/vehiculos/{id_vehiculo}` | Consultar vehículo |
| POST | `/vehiculos/` | Crear vehículo |
| PUT | `/vehiculos/{id_vehiculo}` | Actualizar vehículo |
| DELETE | `/vehiculos/{id_vehiculo}` | Eliminar vehículo |

### 6.2. Comandos

| Método | Endpoint | Función |
|---|---|---|
| GET | `/comandos/vehiculo/{id_vehiculo}` | Consultar comandos |
| POST | `/comandos/` | Crear comando |
| PUT | `/comandos/{id_comando}` | Actualizar comando |
| DELETE | `/comandos/{id_comando}` | Eliminar comando |

### 6.3. Estado e historial

| Método | Endpoint | Función |
|---|---|---|
| GET | `/estado/vehiculo/{id_vehiculo}` | Consultar último estado |
| POST | `/estado/movimiento` | Registrar movimiento individual |
| GET | `/historial/vehiculo/{id_vehiculo}` | Consultar máximo diez movimientos recientes |

### 6.4. DEMOS

| Método | Endpoint | Función |
|---|---|---|
| GET | `/demos/vehiculo/{id_vehiculo}` | Listar DEMOS |
| GET | `/demos/{id_demo}/movimientos` | Consultar movimientos de DEMO |
| POST | `/demos` | Crear DEMO |
| PUT | `/demos/{id_demo}` | Actualizar DEMO |
| DELETE | `/demos/{id_demo}` | Eliminar DEMO |
| POST | `/demos/movimientos` | Agregar movimiento |
| PUT | `/demos/movimientos/{id_demo_movimiento}` | Actualizar movimiento |
| DELETE | `/demos/movimientos/{id_demo_movimiento}` | Eliminar movimiento |
| POST | `/demos/ejecutar` | Ejecutar DEMO |
| POST | `/demos/cancelar/{id_vehiculo}` | Cancelar DEMO |
| GET | `/demos/ejecucion/{id_vehiculo}` | Consultar ejecución |

### 6.5. WebSocket

```text
/ws/vehiculo/{id_vehiculo}
```

Permite establecer una conexión de monitoreo por vehículo y recibir eventos en tiempo real.

Las operaciones protegidas requieren el encabezado:

```http
X-API-Key: tu_clave_api
```

---

## 7. Procedimientos almacenados MySQL

El proyecto integra **21 procedimientos almacenados** en Amazon RDS, distribuidos de la siguiente manera:

| Categoría | Cantidad |
|---|---:|
| Vehículos | 5 |
| Comandos | 4 |
| Estado | 2 |
| Historial | 2 |
| DEMOS | 4 |
| Movimientos DEMO | 4 |
| **Total** | **21** |

La ejecución se centraliza mediante `StoredProcedureRepository`.

La base de datos `vehiculo_iot` contiene seis tablas:

1. `vehiculos`
2. `comandos`
3. `estado_vehiculo`
4. `historial_comandos`
5. `demos`
6. `demo_movimientos`

Durante el Examen Práctico 2.6 se comprobó desde Amazon EC2 la existencia de las seis tablas y los 21 procedimientos almacenados.

La aplicación utiliza los procedimientos almacenados para consultar y administrar información, actualizar estados, registrar historial y ejecutar DEMOS.

---

## 8. Publicación pública en Amazon EC2

### 8.1. Infraestructura utilizada

La API se encuentra desplegada en una instancia Amazon EC2 con las siguientes características:

| Característica | Configuración |
|---|---|
| Servicio | Amazon EC2 |
| Sistema operativo | Windows Server 2025 |
| Tipo de instancia | t3.micro |
| Región | us-east-1 (N. Virginia) |
| Servidor de aplicaciones | Uvicorn / FastAPI |
| Proxy inverso | Caddy |
| Base de datos | Amazon RDS MySQL |
| DNS | Duck DNS |
| Certificado TLS | Let's Encrypt |

### 8.2. Direcciones públicas

**Swagger UI:**

https://vehiculo-iot.duckdns.org/docs

**API REST:**

https://vehiculo-iot.duckdns.org

**WebSocket seguro:**

```text
wss://vehiculo-iot.duckdns.org/ws/vehiculo/1
```

Las direcciones públicas permiten utilizar la aplicación desde clientes externos sin necesidad de acceder mediante `localhost`.

---

## 9. Configuración de Duck DNS

Se utilizó Duck DNS para registrar el subdominio:

```text
vehiculo-iot.duckdns.org
```

El registro DNS apunta a la dirección IP elástica de Amazon EC2:

```text
54.146.69.52
```

Duck DNS proporciona la resolución del nombre público hacia la instancia EC2.

La conexión segura no depende de Duck DNS directamente, sino del certificado TLS administrado por Caddy.

---

## 10. Configuración de Caddy

Caddy se utiliza como proxy inverso para publicar FastAPI mediante HTTPS y WebSocket seguro.

### 10.1. Ubicación

```text
C:\Caddy\
```

Archivos principales:

```text
C:\Caddy\caddy.exe
C:\Caddy\Caddyfile
```

### 10.2. Configuración utilizada

Contenido de `Caddyfile`:

```caddyfile
vehiculo-iot.duckdns.org {
    reverse_proxy 127.0.0.1:8000
}
```

### 10.3. Funcionamiento

Caddy realiza las siguientes funciones:

- Recibe conexiones HTTPS por el puerto 443.
- Gestiona certificados TLS automáticamente.
- Redirige las solicitudes hacia FastAPI.
- Permite conexiones WebSocket seguras.
- Facilita el uso de un mismo dominio para GET, POST y WebSocket.

Durante la configuración se obtuvo correctamente un certificado TLS mediante Let's Encrypt.

### 10.4. Validación de la configuración

```powershell
& "C:\Caddy\caddy.exe" validate --config "C:\Caddy\Caddyfile" --adapter caddyfile
```

Resultado obtenido:

```text
Valid configuration
```

### 10.5. Ejecución manual

```powershell
& "C:\Caddy\caddy.exe" run --config "C:\Caddy\Caddyfile" --adapter caddyfile
```

En el despliegue final Caddy se ejecuta automáticamente mediante Windows Task Scheduler, por lo que no es necesario mantener abierta una terminal PowerShell.

---

## 11. Ejecución persistente en Amazon EC2

Se configuró el Programador de tareas de Windows Server para ejecutar automáticamente FastAPI y Caddy.

### 11.1. Tarea FastAPI

**Nombre:**

```text
Vehiculo-IoT-API
```

**Programa:**

```text
C:\Proyectos\vehiculo_iot_api\.venv\Scripts\python.exe
```

**Argumentos:**

```text
-m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Directorio de trabajo:**

```text
C:\Proyectos\vehiculo_iot_api
```

### 11.2. Tarea Caddy

**Nombre:**

```text
Caddy-HTTPS-WSS
```

**Programa:**

```text
C:\Caddy\caddy.exe
```

**Argumentos:**

```text
run --config "C:\Caddy\Caddyfile" --adapter caddyfile
```

**Directorio de trabajo:**

```text
C:\Caddy
```

### 11.3. Verificación de persistencia

Se comprobó que ambas tareas:

- Se encuentran habilitadas.
- Están configuradas para ejecutarse al iniciar Windows Server.
- Permiten mantener FastAPI y Caddy sin ejecutar manualmente sus comandos.
- Mantienen operativos HTTPS y WSS después de desconectar el Escritorio Remoto.
- Se iniciaron correctamente después de reiniciar Windows Server.

Después del reinicio se comprobó que Swagger UI estaba disponible mediante HTTPS y que el WebSocket seguro permitía establecer una nueva conexión y recibir el estado inicial del vehículo.

---

## 12. Comunicación WebSocket

### 12.1. Dirección local

```text
ws://127.0.0.1:8000/ws/vehiculo/1
```

### 12.2. Dirección pública segura

```text
wss://vehiculo-iot.duckdns.org/ws/vehiculo/1
```

El identificador final corresponde al vehículo que se desea monitorear.

### 12.3. Eventos WebSocket

| Evento | Descripción |
|---|---|
| `estado_inicial` | Envía el último estado guardado en Amazon RDS |
| `movimiento_individual` | Notifica un movimiento individual registrado mediante POST |
| `demo_iniciado` | Indica el inicio de una DEMO |
| `demo_movimiento` | Transmite cada movimiento de la DEMO |
| `demo_finalizado` | Indica la finalización correcta de una DEMO |
| `demo_cancelado` | Notifica la cancelación de una DEMO |
| `demo_error` | Informa un error durante la ejecución |

Los eventos se transmiten mediante mensajes JSON.

### 12.4. Ejemplo de estado inicial

```json
{
  "tipo": "estado_inicial",
  "id_vehiculo": 1,
  "estado": {
    "vehiculo": "Excavadora IoT",
    "id_comando": 9,
    "comando": "DETENER",
    "codigo": 9,
    "conectado": 1
  }
}
```

### 12.5. Ejemplo de movimiento individual

```json
{
  "tipo": "movimiento_individual",
  "id_vehiculo": 1,
  "movimiento": {
    "comando": "AVANZAR",
    "codigo": 1,
    "persistido": true
  }
}
```

### 12.6. Ejemplo de movimiento DEMO

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

Los mensajes reales pueden contener información adicional del comando y marcas temporales.

---

## 13. Movimientos individuales

Los movimientos individuales se ejecutan mediante el endpoint:

```http
POST /estado/movimiento
```

### Ejemplo de solicitud

```json
{
  "id_vehiculo": 1,
  "id_comando": 1,
  "origen": "API"
}
```

### Funcionamiento

1. FastAPI recibe y valida la solicitud.
2. Verifica el vehículo y el comando.
3. Ejecuta los procedimientos almacenados correspondientes.
4. Actualiza el último estado del vehículo.
5. Registra el movimiento en el historial individual.
6. Confirma la persistencia.
7. Notifica el movimiento a los clientes WebSocket conectados.

La actualización del estado y del historial se realiza mediante una transacción de base de datos.

---

## 14. Ejecución de DEMOS

Las DEMOS permiten ejecutar secuencias automatizadas de movimientos.

### Endpoint

```http
POST /demos/ejecutar
```

### Ejemplo de solicitud

```json
{
  "id_vehiculo": 1,
  "id_demo": 1
}
```

### Funcionamiento

1. FastAPI recibe la solicitud de ejecución.
2. Valida el vehículo y la DEMO.
3. Obtiene los movimientos mediante `sp_obtener_movimientos_demo`.
4. Transmite el evento `demo_iniciado`.
5. Ejecuta los movimientos en el orden configurado.
6. Respeta sus duraciones y pausas.
7. Actualiza el último estado del vehículo.
8. Envía cada movimiento mediante WebSocket.
9. Transmite el evento `demo_finalizado` al concluir.

**Los movimientos de DEMO no se agregan al historial individual.**

Esto permite distinguir los movimientos solicitados individualmente de las secuencias automatizadas.

---

## 15. Pruebas funcionales — Examen Práctico 2.6

Las pruebas se realizaron desde una computadora externa utilizando Thunder Client y conexiones WebSocket seguras.

### 15.1. Prueba 1 — POST HTTPS y dos clientes WSS

**Endpoint:**

```http
POST https://vehiculo-iot.duckdns.org/estado/movimiento
```

**Cuerpo JSON:**

```json
{
  "id_vehiculo": 1,
  "id_comando": 1,
  "origen": "API"
}
```

**Resultados:**

- Thunder Client respondió HTTP 200 OK.
- Se registró el movimiento AVANZAR.
- El último estado del vehículo fue actualizado.
- Dos clientes WSS recibieron simultáneamente el evento `movimiento_individual`.
- La persistencia se comprobó mediante la respuesta de la API y el historial.

### 15.2. Prueba 2 — GET HTTPS de historial reciente

**Endpoint:**

```http
GET https://vehiculo-iot.duckdns.org/historial/vehiculo/1
```

**Resultados:**

- Respuesta HTTP 200 OK.
- Se recuperaron diez movimientos individuales.
- Los registros aparecieron ordenados del más reciente al más antiguo.
- El historial contenía movimientos AVANZAR, RETROCEDER, DETENER, ABRIR_PALA y SUBIR_BRAZO.
- La consulta no realiza operaciones de eliminación.

El registro más reciente durante la prueba tenía el identificador `48`, correspondiente a AVANZAR.

### 15.3. Prueba 3 — DEMO mediante HTTPS y WSS

**Endpoint:**

```http
POST https://vehiculo-iot.duckdns.org/demos/ejecutar
```

**Cuerpo JSON:**

```json
{
  "id_vehiculo": 1,
  "id_demo": 1
}
```

**Resultados:**

- Respuesta HTTP 200 OK.
- DEMO principal ejecutada.
- Ocho movimientos programados.
- Recepción de eventos `demo_iniciado`, `demo_movimiento` y `demo_finalizado`.
- Último movimiento: DETENER.
- Actualización del último estado en Amazon RDS.
- La DEMO no agregó nuevos movimientos al historial individual.

---

## 16. Cancelación de DEMO

Se comprobó el funcionamiento del endpoint:

```http
POST /demos/cancelar/{id_vehiculo}
```

### Prueba realizada

Se inició una DEMO de ocho movimientos y se solicitó su cancelación mientras estaba ejecutándose.

**Resultados obtenidos:**

- POST de inicio: HTTP 200 OK.
- POST de cancelación: HTTP 200 OK.
- Respuesta: Cancelación solicitada.
- La DEMO se canceló después de recibir tres movimientos.
- WebSocket notificó el evento `demo_cancelado`.
- Se detuvo la ejecución de los movimientos restantes.
- El último estado del vehículo fue DETENER.

Esto demuestra que la API permite interrumpir una ejecución sin completar toda la secuencia programada.

---

## 17. Control de simultaneidad de DEMOS

Se realizaron dos solicitudes para ejecutar la misma DEMO en el mismo vehículo.

### Primera solicitud

```http
POST /demos/ejecutar
```

**Resultado:** HTTP 200 OK.

### Segunda solicitud

Se envió mientras la primera DEMO continuaba ejecutándose.

**Resultado:** HTTP 400 Bad Request.

**Mensaje recibido:**

```text
Ya existe una DEMO ejecutándose o finalizando para este vehículo.
```

Esto confirma que la API impide ejecutar dos DEMOS simultáneas sobre el mismo vehículo.

---

## 18. Validación y seguridad

Se implementaron y utilizaron diferentes mecanismos de protección para el sistema.

### Seguridad de la API

- Validación de solicitudes mediante Pydantic.
- Operaciones protegidas mediante `X-API-Key`.
- Validación de vehículos y comandos.
- Manejo de respuestas de error.
- Separación de lógica de negocio y acceso a datos.

### Seguridad de comunicación

- HTTPS para solicitudes REST.
- WSS para comunicación WebSocket.
- Certificados TLS gestionados por Caddy.
- FastAPI escuchando internamente en `127.0.0.1:8000`.

### Seguridad de credenciales

- Variables de entorno para la conexión MySQL.
- Archivo `.env` excluido del repositorio.
- Archivo `.env.example` sin credenciales reales.
- No publicar contraseñas, API Keys ni tokens en GitHub o evidencias.

### Seguridad de infraestructura

- Grupos de seguridad de Amazon EC2.
- Reglas de acceso para Amazon RDS.
- Puerto 3306 destinado a la conexión con MySQL.
- Puertos 80 y 443 utilizados para la publicación web.

**Nota:** Antes de una implementación productiva se deben revisar y restringir las reglas de acceso de EC2 y RDS, especialmente los puertos que no necesitan estar disponibles públicamente.

---

## 19. Herramientas de prueba

Se utilizaron diferentes herramientas para comprobar el funcionamiento del proyecto:

**Swagger UI:** documentación interactiva y pruebas de endpoints GET, POST, PUT y DELETE.

**Thunder Client:** pruebas HTTP mediante HTTPS, incluyendo movimientos individuales, historial, DEMOS y cancelaciones.

**HTTP Client de Google Chrome:** establecimiento de conexiones WSS y visualización de eventos en tiempo real.

**PowerShell:** comprobaciones de conectividad, ejecución de servicios y tareas programadas.

**MySQL / PyMySQL:** consultas a Amazon RDS y verificación de tablas y procedimientos almacenados.

---

## 20. Resultados obtenidos

Durante el desarrollo y migración del proyecto se consiguió:

- Migrar FastAPI desde el entorno de desarrollo local a Amazon EC2.
- Conectar la aplicación con Amazon RDS MySQL.
- Verificar seis tablas y 21 procedimientos almacenados.
- Publicar Swagger UI mediante HTTPS.
- Habilitar WebSocket seguro mediante WSS.
- Transmitir movimientos individuales en tiempo real.
- Mantener dos conexiones WebSocket simultáneas.
- Ejecutar DEMOS de ocho movimientos.
- Actualizar el último estado sin registrar movimientos DEMO en el historial.
- Cancelar DEMOS durante su ejecución.
- Impedir dos DEMOS simultáneas sobre un mismo vehículo.
- Configurar el inicio automático de FastAPI y Caddy.
- Comprobar que HTTPS y WSS continúan funcionando después de reiniciar Windows Server.

---

## 21. Alcance del proyecto

La API representa una solución de administración y comunicación para vehículos IoT.

WebSocket constituye el canal lógico que podría utilizarse posteriormente para transmitir instrucciones a dispositivos físicos como ESP8266 o ESP32.

El Examen Práctico 2.6 no requiere implementar la conexión física con los motores ni recibir confirmación de los actuadores.

La solución se enfoca en la comunicación, administración de estados, persistencia de datos y ejecución automatizada de movimientos mediante servicios públicos y seguros.

---

## 22. Conclusión

El desarrollo y migración de la API REST para Vehículo IoT permitió aplicar conocimientos de Python, FastAPI, Programación Orientada a Objetos, bases de datos MySQL y servicios de Amazon Web Services en un entorno real de despliegue.

Durante la Práctica 2.5 se construyó una aplicación modular capaz de administrar vehículos, comandos, estados, historial y DEMOS utilizando procedimientos almacenados en Amazon RDS.

Posteriormente, en el Examen Práctico 2.6, esta misma aplicación fue migrada a Amazon EC2 con Windows Server 2025 y publicada mediante HTTPS y WebSocket seguro, utilizando Duck DNS y Caddy.

Las pruebas realizadas permitieron comprobar la comunicación en tiempo real, la ejecución de movimientos individuales, las secuencias automatizadas, la cancelación de DEMOS y el control de simultaneidad.

También se verificó que la aplicación permanece funcionando después de cerrar la sesión de Escritorio Remoto y reiniciar Windows Server, gracias a la configuración de tareas programadas.

En conclusión, esta actividad permitió comprender cómo integrar desarrollo de software, infraestructura en la nube, bases de datos, protocolos de comunicación y mecanismos de seguridad para implementar una solución IoT accesible desde Internet, escalable en su arquitectura y preparada para futuras integraciones con dispositivos físicos.

---

## 23. Repositorio GitHub

**Repositorio del proyecto:**

https://github.com/OscarM988/vehiculo_iot_api

El repositorio contiene el código fuente, las dependencias, la estructura modular y la documentación correspondiente a la Práctica 2.5 y el Examen Práctico 2.6.

El archivo `.env` y las credenciales privadas no deben incluirse en el repositorio.

---

**Proyecto académico — Tecnológico Nacional de México, campus Pachuca**

**Ingeniería en Sistemas Computacionales**

**Materia: Implementación de Soluciones IoT**