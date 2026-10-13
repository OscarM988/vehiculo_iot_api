
from fastapi import FastAPI
from app.routers import vehiculos, comandos, estado, historial, demos, websocket

app = FastAPI(
    title="API Vehículo IoT",
    description="Práctica 2.5 - FastAPI, POO, Amazon RDS y WebSocket",
    version="1.0.0"
)

app.include_router(vehiculos.router)
app.include_router(comandos.router)
app.include_router(estado.router)
app.include_router(historial.router)
app.include_router(demos.router)
app.include_router(websocket.router)

@app.get("/", tags=["General"])
def inicio():
    return {
        "mensaje": "API Vehículo IoT funcionando correctamente",
        "estado": "activo"
    }
