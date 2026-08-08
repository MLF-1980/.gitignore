import http.server
import json
import os
from urllib.parse import urlparse, parse_qs

class ApplicationHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.serve_html()
        elif parsed_path.path == '/api/data':
            self.serve_json()
        else:
            self.send_error(404, "Página no encontrada")

    def serve_html(self):
        html_path = os.path.join(os.path.dirname(__file__), '../../templates/index.html')
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        else:
            self.send_error(404, "Archivo HTML no encontrado")

    def serve_json(self):
        data = {"status": "success", "message": "Datos desde la API"}
        response = json.dumps(data)
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))