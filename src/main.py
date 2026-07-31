from src.api.router import router as personal_router
from src.domain.exceptions import DomainError, UserNotFoundError
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from src.infrastructure.database import Base, engine, get_db
from src.infrastructure.repositories import SQLAlchemyPersonalRepository

from sqlalchemy.orm import Session

# Crear las tablas automáticamente en SQLite al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SafeCore API", version="1.0.0")

app.include_router(personal_router)

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
  return JSONResponse(
      status_code=404,
     content={"codigo": "SAFECORE_NOT_FOUND", "sistema": "SafeCore Subcontratistas", "detalle": str(exc)},
  )


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
  return JSONResponse(
      status_code=400,
     content={"codigo": "SAFECORE_REGULATORY_VIOLATION", "sistema": "SafeCore Subcontratistas", "detalle": str(exc)},
  )


@app.get("/")
def health_check():
  return {"status": "SafeCore running successfully"}