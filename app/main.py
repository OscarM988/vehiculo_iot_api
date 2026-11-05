from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    vehiculos,
    comandos,
    estado,
    historial,
    demos,
    websocket
)

app = FastAPI(
    title="API Vehículo IoT",
    description="Práctica 2.5 - FastAPI, POO, Amazon RDS y WebSocket",
    version="1.0.0"
)

# ---------------------------------------------
# CONFIGURACIÓN CORS - GITHUB PAGES
# ---------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://oscarm988.github.io"
    ],
    allow_credentials=False,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE"
    ],
    allow_headers=[
        "Content-Type",
        "X-API-Key"
    ]
)

# ---------------------------------------------
# REGISTRO DE ROUTERS
# ---------------------------------------------

app.include_router(vehiculos.router)
app.include_router(comandos.router)
app.include_router(estado.router)
app.include_router(historial.router)
app.include_router(demos.router)
app.include_router(websocket.router)

# ---------------------------------------------
# ENDPOINT PRINCIPAL
# ---------------------------------------------

@app.get("/", tags=["General"])
def inicio():
    return {
        "mensaje": "API Vehículo IoT funcionando correctamente",
        "estado": "activo"
    }