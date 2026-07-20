from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="SafeCore API",
    description="API REST con Arquitectura Limpia para el control de trabajadores",
    version="1.0.0"
)

# Definimos el esquema de datos que esperamos recibir (DTO)
class TrabajadorDTO(BaseModel):
    id_trabajador: str
    nombre: str
    meses_epp: int
    activo: bool

@app.get("/")
def leer_raiz():
    return {"mensaje": "¡Bienvenido a la API de SafeCore con Arquitectura Limpia!"}

@app.post("/trabajadores/")
def registrar_trabajador(trabajador: TrabajadorDTO):
    # Aquí es donde en un sistema completo llamarías a tu Caso de Uso:
    # repo = JsonRepository()
    # use_case = RegistrarTrabajador(repo)
    # ...
    
    return {
        "estado": "¡Éxito!",
        "mensaje": f"El trabajador {trabajador.nombre} ha sido procesado correctamente por el núcleo de la aplicación.",
        "detalle": trabajador
    }