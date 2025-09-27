#!/usr/bin/env python3
"""
Cliente de prueba para Socket.IO
"""

import socketio
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SocketIO-Test")

def test_socketio_connection():
    try:
        print("🚀 INICIANDO PRUEBA SOCKET.IO")
        print("=" * 50)
        
        # Crear cliente Socket.IO
        sio = socketio.Client(logger=True, engineio_logger=True)
        
        @sio.event
        def connect():
            print("✅ ✅ ✅ CONEXIÓN EXITOSA")
            print("🔥 Servidor Socket.IO aceptó la conexión")
            
            # Registrar usuario de prueba
            sio.emit('register', {'username': 'Usuario_Prueba'})
            print("📝 Usuario de prueba registrado")
            
        @sio.event
        def connect_error(data):
            print(f"❌ ERROR DE CONEXIÓN: {data}")
            
        @sio.event
        def disconnect():
            print("🔌 Desconectado del servidor")
            
        @sio.event
        def users_list(data):
            print(f"📋 LISTA DE USUARIOS: {data}")
            
        @sio.event
        def user_joined(data):
            print(f"🎉 NUEVO USUARIO: {data}")
            
        @sio.event
        def chat_message(data):
            print(f"💬 MENSAJE RECIBIDO: {data}")
            
        @sio.event
        def users_update(data):
            print(f"👥 ACTUALIZACIÓN USUARIOS: {data['count']} conectados")

        print("🔗 Conectando a: https://chat-multiplataforma.onrender.com")
        print("⏳ Esperando respuesta...")
        
        # Conectar con timeout
        sio.connect(
            'https://chat-multiplataforma.onrender.com',
            wait_timeout=10
        )
        
        # Esperar eventos
        print("🕒 Esperando eventos por 5 segundos...")
        time.sleep(5)
        
        # Enviar mensaje de prueba
        print("📤 Enviando mensaje de prueba...")
        sio.emit('chat_message', {'message': 'Hola desde el test!'})
        
        # Esperar un poco más
        time.sleep(2)
        
        # Desconectar
        sio.disconnect()
        print("✅ ✅ ✅ PRUEBA COMPLETADA EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"💥 ERROR FATAL: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Cliente de prueba Socket.IO para Render")
    print("💡 Asegúrate de que el servidor esté desplegado")
    print("=" * 50)
    
    success = test_socketio_connection()
    
    print("=" * 50)
    if success:
        print("🎉 ¡TODO FUNCIONA CORRECTAMENTE!")
    else:
        print("😞 Hay problemas que resolver")
