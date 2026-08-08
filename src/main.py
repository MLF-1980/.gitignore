import http.server
from src.infrastructure.database import init_db
from src.api.handlers import ApplicationHandler

PORT = 8000

def run():
    # Inicializar base de datos
    init_db()
    
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, ApplicationHandler)
    print(f"Servidor corriendo en http://localhost:{PORT}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")
        httpd.server_close()

if __name__ == '__main__':
    run()