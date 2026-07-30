from typing import List
from application.schemas import PersonalCreate, PersonalResponse
from fastapi import APIRouter, Depends
from infrastructure.database import get_db
from infrastructure.repositories import SQLAlchemyPersonalRepository
from sqlalchemy.orm import Session

router = APIRouter(prefix="/personal", tags=["Personal"])


@router.post("/", response_model=PersonalResponse)
def crear_personal(personal: PersonalCreate, db: Session = Depends(get_db)):
  repo = SQLAlchemyPersonalRepository(db)
  return repo.guardar(personal)


@router.get("/", response_model=List[PersonalResponse])
def listar_personal(db: Session = Depends(get_db)):
  repo = SQLAlchemyPersonalRepository(db)
  return repo.obtener_todos()