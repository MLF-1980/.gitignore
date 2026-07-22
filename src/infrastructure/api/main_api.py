from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.infrastructure.repositories import JSONTrabajadorRepository
from src.domain.entities import Trabajador

app = FastAPI(
    title="SafeCore API",
    description="API REST conectada al repositorio JSON con Arquitectura Limpia",
    version="1.0.0"
)

# Inicializamos el repositorio apuntando a la base de datos en la raíz
repo = JSONTrabajadorRepository("safecore_db.json")

class TrabajadorDTO(BaseModel):
    id_trabajador: str
    nombre: str
    meses_uso_epp: int
    induccion_aprobada: bool

@app.get("/")
def leer_raiz():
    return {"mensaje": "¡SafeCore API operando con persistencia real!"}

@app.post("/trabajadores/")
def registrar_trabajador(trabajador_dto: TrabajadorDTO):
    try:
        # Creamos la entidad utilizando los datos del DTO
        trabajador = Trabajador(
            id_trabajador=trabajador_dto.id_trabajador,
            nombre=trabajador_dto.nombre,
            meses_uso_epp=trabajador_dto.meses_uso_epp,
            induccion_aprobada=trabajador_dto.induccion_aprobada
        )
        
        repo.guardar(trabajador)
        
        return {
            "estado": "Registrado con éxito en el archivo JSON",
            "datos": trabajador_dto
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))