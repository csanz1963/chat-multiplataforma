import asyncio
import websockets
import json
import tkinter as tk
from tkinter import messagebox
import threading
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ChatClientCloud")

class ChatClientCloud:
    def __init__(self):
        self.websocket = None
        self.username = None
        self.server_url = None
        self.connected = False
        self.chat_window = None
        self.loop = None
        
    async def connect_to_server(self):
        try:
            if not self.server_url:
                self.server_url = "ws://localhost:8765"
            
            logger.info(f"Conectando a {self.server_url}...")
            self.websocket = await websockets.connect(
                self.server_url, 
                ping_interval=20, 
                ping_timeout=10
            )
            self.connected = True
            
            register_msg = {
                "type": "register", 
                "username": self.username
            }
            await self.websocket.send(json.dumps(register_msg))
            logger.info(f"Registrado como: {self.username}")
            return True
            
        except Exception as e:
            logger.error(f"Error de conexion: {e}")
            self.connected = False
            return False
    
    async def listen_for_messages(self):
        while self.connected:
            try:
                message = await asyncio.wait_for(
                    self.websocket.recv(), 
                    timeout=1.0
                )
                data = json.loads(message)
                
                if self.chat_window:
                    self.chat_window.handle_server_message(data)
                    
            except asyncio.TimeoutError:
                continue
            except websockets.exceptions.ConnectionClosed:
                logger.warning("Conexion con el servidor cerrada")
                self.connected = False
                if self.chat_window:
                    self.chat_window.show_error("Conexion perdida con el servidor")
                break
            except Exception as e:
                logger.error(f"Error escuchando mensajes: {e}")
                self.connected = False
                break
    
    async def send_message(self, message):
        if self.connected and self.websocket:
            try:
                message_data = {
                    "type": "chat_message",
                    "message": message
                }
                await self.websocket.send(json.dumps(message_data))
                logger.info(f"Mensaje enviado: {message[:50]}...")
                return True
            except Exception as e:
                logger.error(f"Error al enviar mensaje: {e}")
                self.connected = False
                return False
        return False
    
    def disconnect(self):
        logger.info("Desconectando del servidor...")
        self.connected = False
        if self.websocket and self.loop:
            asyncio.run_coroutine_threadsafe(
                self.websocket.close(), 
                self.loop
            )

if __name__ == "__main__":
    print("Cliente Chat Cloud")
