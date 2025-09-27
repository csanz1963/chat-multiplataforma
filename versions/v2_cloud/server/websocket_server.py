import os
import asyncio
import websockets
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ChatServerCloud")

class ChatServerCloud:
    def __init__(self, host='0.0.0.0', port=8765):
        self.host = host
        self.port = port
        self.clients = set()
        self.usernames = {}
        
    async def register(self, websocket, username):
        self.clients.add(websocket)
        self.usernames[websocket] = username
        logger.info(f"Usuario conectado: {username}. Total: {len(self.clients)}")
        
        if len(self.clients) > 1:
            await asyncio.sleep(0.4)
        
        await self.send_welcome_message(websocket, username)
        
        if len(self.clients) > 1:
            join_message = {
                "type": "user_joined",
                "username": username,
                "users_online": list(self.usernames.values()),
                "is_new": True
            }
            await self.broadcast_to_others(websocket, join_message)
    
    async def send_welcome_message(self, websocket, username):
        try:
            other_users = [u for u in self.usernames.values() if u != username]
            
            if other_users:
                users_message = {
                    "type": "users_list",
                    "users_online": list(self.usernames.values()),
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send(json.dumps(users_message))
            
            for existing_user in other_users:
                user_joined_message = {
                    "type": "user_joined",
                    "username": existing_user,
                    "users_online": list(self.usernames.values()),
                    "is_existing": True
                }
                await websocket.send(json.dumps(user_joined_message))
                
        except Exception as e:
            logger.error(f"Error en bienvenida: {e}")
    
    async def broadcast_to_others(self, exclude_websocket, message):
        if len(self.clients) <= 1:
            return
            
        message_json = json.dumps(message)
        disconnected = []
        
        for client in self.clients:
            if client != exclude_websocket:
                try:
                    await client.send(message_json)
                except websockets.exceptions.ConnectionClosed:
                    disconnected.append(client)
        
        for client in disconnected:
            await self.unregister(client)
    
    async def broadcast(self, message):
        if self.clients:
            message_json = json.dumps(message)
            disconnected = []
            
            for client in self.clients:
                try:
                    await client.send(message_json)
                except websockets.exceptions.ConnectionClosed:
                    disconnected.append(client)
            
            for client in disconnected:
                await self.unregister(client)
    
    async def unregister(self, websocket):
        if websocket in self.clients:
            username = self.usernames.get(websocket, "Unknown")
            self.clients.remove(websocket)
            if websocket in self.usernames:
                del self.usernames[websocket]
            
            logger.info(f"Usuario desconectado: {username}. Total: {len(self.clients)}")
            
            if self.clients:
                message = {
                    "type": "user_left",
                    "username": username,
                    "users_online": list(self.usernames.values())
                }
                await self.broadcast(message)
    
    async def handle_message(self, websocket, message_data):
        username = self.usernames.get(websocket, "Unknown")
        
        if message_data["type"] == "chat_message":
            logger.info(f"Mensaje de {username}: {message_data['message']}")
            message = {
                "type": "chat_message",
                "username": username,
                "message": message_data["message"],
                "timestamp": datetime.now().isoformat()
            }
            await self.broadcast(message)
    
    async def handler(self, websocket):
        client_ip = websocket.remote_address[0] if websocket.remote_address else "Unknown"
        logger.info(f"Nueva conexion desde: {client_ip}")
        
        try:
            async for message in websocket:
                data = json.loads(message)
                
                if data["type"] == "register":
                    await self.register(websocket, data["username"])
                    break
            
            async for message in websocket:
                data = json.loads(message)
                await self.handle_message(websocket, data)
                
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            await self.unregister(websocket)
    
    async def start_server(self):
        logger.info(f"Iniciando servidor Cloud en {self.host}:{self.port}")
        
        port = int(os.environ.get('PORT', self.port))
        
        async with websockets.serve(self.handler, self.host, port):
            logger.info(f"Servidor Cloud activo en puerto {port}")
            await asyncio.Future()

def main():
    print("Chat Multiplataforma - Servidor Cloud")
    server = ChatServerCloud()
    
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        logger.info("Servidor detenido")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()
