from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from src.infrastructure.repositories import JSONTrabajadorRepository
from src.domain.entities import Trabajador, Nombre, MesesUsoEPP
from src.application.use_cases import RegistrarTrabajador

app = FastAPI(
    title="SafeCore API",
    description="API REST conectada al repositorio JSON con Arquitectura Limpia",
    version="1.0.0"
)

# Función de inyección de dependencias para el repositorio
def obtener_repositorio():
    return JSONTrabajadorRepository("safecore_db.json")

class TrabajadorDTO(BaseModel):
    id_trabajador: str
    nombre: str
    meses_uso_epp: int
    induccion_aprobada: bool

@app.get("/")
def leer_raiz():
    return {"mensaje": "SafeCore API operando con persistencia real!"}

@app.post("/trabajadores/")
def registrar_trabajador(
    trabajador_dto: TrabajadorDTO,
    repo: JSONTrabajadorRepository = Depends(obtener_repositorio)
):
    try:
        # Creamos la entidad del dominio utilizando los Value Objects requeridos
        trabajador = Trabajador(
            id_trabajador=trabajador_dto.id_trabajador,
            nombre=Nombre(trabajador_dto.nombre),
            meses_uso_epp=MesesUsoEPP(trabajador_dto.meses_uso_epp),
            induccion_aprobada=trabajador_dto.induccion_aprobada
        )
        
        # Instanciamos el Caso de Uso inyectando el repositorio
        caso_uso = RegistrarTrabajador(repo)
        caso_uso.ejecutar(trabajador)
        
        return {
            "status": "success",
            "message": f"Trabajador {trabajador.id_trabajador} registrado correctamente."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))