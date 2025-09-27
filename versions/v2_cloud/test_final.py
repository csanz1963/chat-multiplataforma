#!/usr/bin/env python3
"""
Test final del chat cloud
"""

import requests
import socketio
import time

def test_final():
    print("🎯 TEST FINAL DEL CHAT CLOUD")
    print("=" * 50)
    
    # 1. Test web básica
    print("1. Probando página web...")
    try:
        r = requests.get('https://chat-multiplataforma.onrender.com', timeout=10)
        if r.status_code == 200:
            print("   ✅ Web OK")
            if "Cloud FIXED" in r.text:
                print("   ✅ Versión NUEVA detectada")
            else:
                print("   ⚠️  Versión vieja (puede ser cache)")
        else:
            print(f"   ❌ Web FAILED: {r.status_code}")
    except Exception as e:
        print(f"   ❌ Web ERROR: {e}")
    
    # 2. Test Socket.IO
    print("2. Probando Socket.IO...")
    try:
        sio = socketio.Client()
        
        @sio.event
        def connect():
            print("   ✅ ✅ ✅ SOCKET.IO CONECTADO!")
            
        @sio.event
        def connect_error(data):
            print(f"   ❌ Socket.IO error: {data}")
            
        sio.connect('https://chat-multiplataforma.onrender.com', wait_timeout=10)
        time.sleep(2)
        sio.disconnect()
        
    except Exception as e:
        print(f"   ❌ Socket.IO FAILED: {e}")
    
    print("=" * 50)
    print("🎉 Test completado - Revisa resultados arriba")

if __name__ == "__main__":
    test_final()
