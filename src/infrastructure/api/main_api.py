from fastapi import FastAPI
from src.api.router import router as personal_router

app = FastAPI(
    title="SafeCore API",
    description="API REST bajo principios de Clean Architecture y SQLAlchemy",
    version="1.0.0"
)

# Incluimos el router centralizado de la API
app.include_router(personal_router)

@app.get("/")
def leer_raiz():
    return {"mensaje": "SafeCore API operando con Clean Architecture y Base de Datos Relacional!"}