
from collections import defaultdict
from datetime import datetime, timezone

from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder


class WebSocketManager:

    def __init__(self):
        self.conexiones = defaultdict(set)

    async def conectar(self, websocket: WebSocket, id_vehiculo: int):
        await websocket.accept()
        self.conexiones[id_vehiculo].add(websocket)

    def desconectar(self, websocket: WebSocket, id_vehiculo: int):
        clientes = self.conexiones.get(id_vehiculo)

        if clientes is not None:
            clientes.discard(websocket)

            if not clientes:
                self.conexiones.pop(id_vehiculo, None)

    async def enviar_a_vehiculo(self, id_vehiculo: int, mensaje: dict):
        clientes = list(self.conexiones.get(id_vehiculo, set()))

        mensaje_json = jsonable_encoder(mensaje)

        for websocket in clientes:
            try:
                await websocket.send_json(mensaje_json)

            except Exception:
                self.desconectar(websocket, id_vehiculo)

    def crear_evento(self, tipo: str, id_vehiculo: int, **datos):
        return {
            "tipo": tipo,
            "id_vehiculo": id_vehiculo,
            **datos,
            "fecha_hora": datetime.now(timezone.utc).isoformat()
        }


websocket_manager = WebSocketManager()
