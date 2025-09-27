import os
from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ChatServerUnified")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat-secret-key-123'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Estado del chat
clients = {}
usernames = {}

@app.route('/')
def index():
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat Multiplataforma - Cloud</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 40px; 
                background: #667eea;
                color: white;
                text-align: center;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 15px;
            }
            .status { 
                background: #27ae60; 
                padding: 10px; 
                border-radius: 5px; 
                margin: 20px 0;
            }
            .info { background: #34495e; padding: 15px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✅ Chat Multiplataforma - Cloud</h1>
            <div class="status">
                <h2>Servidor Unificado Activo</h2>
                <p>Flask + WebSocket en un único servidor</p>
            </div>
            <div class="info">
                <h3>🚀 Funcionando en Render</h3>
                <p><strong>URL:</strong> https://chat-multiplataforma.onrender.com</p>
                <p><strong>WebSocket:</strong> Conectado al mismo puerto</p>
                <p><strong>Usuarios conectados:</strong> <span id="users">0</span></p>
            </div>
            <div style="margin-top: 20px;">
                <p>💡 <strong>Cliente recomendado:</strong> Usa main_red_local.py pero cambia la URL a:</p>
                <code>wss://chat-multiplataforma.onrender.com</code>
            </div>
        </div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.min.js"></script>
        <script>
            const socket = io();
            
            socket.on('connect', function() {
                console.log('Conectado al servidor WebSocket');
                document.getElementById('users').textContent = '1';
            });
            
            socket.on('users_update', function(data) {
                document.getElementById('users').textContent = data.count;
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

@socketio.on('connect')
def handle_connect():
    logger.info(f"✅ Nuevo cliente conectado: {request.sid}")
    clients[request.sid] = request.sid

@socketio.on('disconnect')
def handle_disconnect():
    username = usernames.get(request.sid, 'Unknown')
    if request.sid in clients:
        del clients[request.sid]
    if request.sid in usernames:
        del usernames[request.sid]
    
    logger.info(f"❌ Cliente desconectado: {username}")
    
    # Notificar a todos
    emit('users_update', {
        'count': len(clients),
        'users_online': list(usernames.values())
    }, broadcast=True)
    
    emit('user_left', {
        'username': username,
        'users_online': list(usernames.values())
    }, broadcast=True)

@socketio.on('register')
def handle_register(data):
    username = data.get('username', f'User_{request.sid[:6]}')
    usernames[request.sid] = username
    clients[request.sid] = request.sid
    
    logger.info(f"👤 Usuario registrado: {username}")
    
    # Enviar lista actual al nuevo usuario
    emit('users_list', {
        'users_online': list(usernames.values()),
        'message': f'Bienvenido {username}!'
    })
    
    # Notificar a todos del nuevo usuario
    emit('user_joined', {
        'username': username,
        'users_online': list(usernames.values())
    }, broadcast=True)

@socketio.on('chat_message')
def handle_chat_message(data):
    username = usernames.get(request.sid, 'Unknown')
    message = data.get('message', '')
    
    logger.info(f"💬 Mensaje de {username}: {message}")
    
    emit('chat_message', {
        'username': username,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 Iniciando servidor unificado en puerto {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
