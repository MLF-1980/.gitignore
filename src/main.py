from domain.exceptions import DomainError, UserNotFoundError
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from infrastructure.database import Base, engine, get_db
from infrastructure.repositories import SQLAlchemyPersonalRepository

from sqlalchemy.orm import Session

# Crear las tablas automáticamente en SQLite al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SafeCore API", version="1.0.0")


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
  return JSONResponse(
      status_code=404,
      content={"error": "Not Found", "message": str(exc)},
  )


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
  return JSONResponse(
      status_code=400,
      content={"error": "Business Rule Violation", "message": str(exc)},
  )


@app.get("/")
def health_check():
  return {"status": "SafeCore running successfully"}


@app.post("/personal/")
def crear_personal(
    nombre: str,
    apellido: str,
    dni: str,
    cargo: str,
    db: Session = Depends(get_db),
):
  repo = SQLAlchemyPersonalRepository(db)

  class PersonalDTO:

    def __init__(self, nombre, apellido, dni, cargo):
      self.nombre = nombre
      self.apellido = apellido
      self.dni = dni
      self.cargo = cargo

  nuevo = PersonalDTO(nombre, apellido, dni, cargo)
  resultado = repo.guardar(nuevo)
  return {
      "mensaje": "Personal registrado con éxito en la base de datos",
      "id": resultado.id,
  }


@app.get("/personal/")
def listar_personal(db: Session = Depends(get_db)):
  repo = SQLAlchemyPersonalRepository(db)
  return repo.obtener_todos()