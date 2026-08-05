import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Directorio raíz del proyecto hsa
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Si tenés tu carpeta de imágenes/logo dentro de hsa, descomenta y ajusta esta línea:
# app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    # Buscamos tu index.html dentro de la carpeta hsa
    html_path = os.path.join(BASE_DIR, "index.html")
    
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
            
    return """
    <html>
        <head><title>HSA - Mi Web</title></head>
        <body style="background: #111; color: #fff; text-align: center; padding-top: 50px;">
            <h1>Proyecto HSA</h1>
            <p>Coloca tu archivo index.html en la raíz de la carpeta <b>hsa</b> para que se vea tu diseño y tu logo.</p>
        </body>
    </html>
    """