import os
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat Multiplataforma - Servidor</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 40px; 
                background: #667eea;
                color: white;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 15px;
            }
            h1 { color: #fff; text-align: center; }
            .status { 
                background: #27ae60; 
                padding: 10px; 
                border-radius: 5px; 
                text-align: center;
                margin: 20px 0;
            }
            .info { background: #34495e; padding: 15px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Chat Multiplataforma - Servidor Activo</h1>
            <div class="status">
                <h2>Servidor WebSocket Funcionando</h2>
            </div>
            <div class="info">
                <h3>Informacion de Conexion:</h3>
                <p><strong>URL WebSocket:</strong> ws://localhost:8765</p>
                <p><strong>Puerto:</strong> 8765</p>
                <p><strong>Estado:</strong> <span id="status">Conectando...</span></p>
                <p><strong>Usuarios conectados:</strong> <span id="users">0</span></p>
            </div>
        </div>
        
        <script>
            function connectWebSocket() {
                const hostname = window.location.hostname;
                const ws = new WebSocket('wss://' + hostname + ':8765');
                
                ws.onopen = function() {
                    document.getElementById('status').textContent = 'Conectado';
                    document.getElementById('status').style.color = '#27ae60';
                };
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    if (data.type === 'users_list') {
                        document.getElementById('users').textContent = data.users_online.length;
                    }
                };
                
                ws.onclose = function() {
                    document.getElementById('status').textContent = 'Desconectado';
                    document.getElementById('status').style.color = '#e74c3c';
                    setTimeout(connectWebSocket, 5000);
                };
            }
            
            window.addEventListener('load', connectWebSocket);
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
