#!/usr/bin/env python3
"""
Cliente de prueba para el chat cloud
"""

import asyncio
import websockets
import json
import sys

async def test_connection(server_url):
    try:
        print(f"Probando conexion a {server_url}...")
        async with websockets.connect(server_url) as websocket:
            register_msg = {
                "type": "register",
                "username": "Usuario_Test"
            }
            await websocket.send(json.dumps(register_msg))
            print("Registrado exitosamente")
            
            response = await asyncio.wait_for(websocket.recv(), timeout=10)
            data = json.loads(response)
            print(f"Respuesta del servidor: {data.get('type')}")
            
            return True
            
    except Exception as e:
        print(f"Error de conexion: {e}")
        return False

if __name__ == "__main__":
    server_url = "ws://localhost:8765"
    if len(sys.argv) > 1:
        server_url = sys.argv[1]
    
    asyncio.run(test_connection(server_url))
