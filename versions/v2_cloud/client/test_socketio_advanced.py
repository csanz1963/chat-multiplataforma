#!/usr/bin/env python3
"""
Cliente de prueba avanzado para Socket.IO
"""

import socketio
import time
import requests

def test_web_first():
    """Primero probar que la web funciona"""
    print("🌐 Probando endpoint web...")
    try:
        response = requests.get('https://chat-multiplataforma.onrender.com', timeout=10)
        print(f"✅ Web OK - Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Web FAILED: {e}")
        return False

def test_health_check():
    """Probar endpoint de health check"""
    print("❤️ Probando health check...")
    try:
        response = requests.get('https://chat-multiplataforma.onrender.com/health', timeout=10)
        print(f"✅ Health OK - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"📊 Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health FAILED: {e}")
        return False

def test_socketio_connection():
    """Probar conexión Socket.IO"""
    print("🔌 Probando Socket.IO...")
    try:
        sio = socketio.Client(logger=False)
        
        @sio.event
        def connect():
            print("✅ ✅ ✅ SOCKET.IO CONNECTED!")
            
        @sio.event 
        def connect_error(data):
            print(f"❌ Socket.IO connection error: {data}")
            
        @sio.event
        def disconnect():
            print("🔌 Socket.IO disconnected")
            
        @sio.event
        def connected(data):
            print(f"🎉 Server welcome: {data}")

        print("🔄 Intentando conectar...")
        sio.connect(
            'https://chat-multiplataforma.onrender.com',
            wait_timeout=15,
            transports=['websocket', 'polling']
        )
        
        time.sleep(3)
        
        # Probar registro
        sio.emit('register', {'username': 'TestUser'})
        print("📝 Registro enviado")
        
        time.sleep(2)
        
        # Probar mensaje
        sio.emit('chat_message', {'message': 'Test message'})
        print("💬 Mensaje de prueba enviado")
        
        time.sleep(2)
        sio.disconnect()
        return True
        
    except Exception as e:
        print(f"💥 Socket.IO FAILED: {e}")
        return False

if __name__ == "__main__":
    print("🎯 PRUEBA COMPLETA DEL CHAT CLOUD")
    print("=" * 60)
    
    web_ok = test_web_first()
    health_ok = test_health_check()
    
    if web_ok and health_ok:
        print("\n🔗 Probando Socket.IO (esto puede tomar 15 segundos)...")
        socket_ok = test_socketio_connection()
    else:
        socket_ok = False
        print("\n⏹️ Saltando prueba Socket.IO por fallos previos")
    
    print("=" * 60)
    print("📊 RESUMEN FINAL:")
    print(f"🌐 Web: {'✅' if web_ok else '❌'}")
    print(f"❤️ Health: {'✅' if health_ok else '❌'}") 
    print(f"🔌 Socket.IO: {'✅' if socket_ok else '❌'}")
    
    if web_ok and health_ok and socket_ok:
        print("🎉 ¡TODOS LOS TESTS PASAN! El chat cloud está FUNCIONANDO")
    else:
        print("😞 Algunos tests fallaron - revisar logs de Render")
