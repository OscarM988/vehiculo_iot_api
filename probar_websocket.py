
import asyncio
import json
import websockets


async def probar_conexion():
    url = "ws://127.0.0.1:8000/ws/vehiculo/1"

    try:
        async with websockets.connect(url) as websocket:
            print("Conexión WebSocket establecida")

            mensaje = await asyncio.wait_for(
                websocket.recv(),
                timeout=15
            )

            datos = json.loads(mensaje)

            print("Mensaje recibido:")
            print(json.dumps(datos, indent=4, ensure_ascii=False))

    except Exception as error:
        print("Error de conexión WebSocket:")
        print(type(error).__name__)
        print(str(error))


asyncio.run(probar_conexion())
