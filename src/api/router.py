from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.application.schemas import PersonalCreate, PersonalResponse
from src.application.use_cases import RegistrarTrabajador, ListarTrabajadores, ObtenerTrabajadorPorId
from src.infrastructure.database import get_db
from src.infrastructure.repositories import SQLAlchemyPersonalRepository

router = APIRouter(prefix="/personal", tags=["Personal"])

@router.post("/", response_model=PersonalResponse)
def crear_personal(personal: PersonalCreate, db: Session = Depends(get_db)):
    # 1. Instanciamos el repositorio
    repo = SQLAlchemyPersonalRepository(db)
    # 2. Instanciamos el caso de uso inyectándole el repositorio
    caso_de_uso = RegistrarTrabajador(repo)
    # 3. Ejecutamos la acción de negocio
    return caso_de_uso.ejecutar(personal)

@router.get("/", response_model=List[PersonalResponse])
def listar_personal(db: Session = Depends(get_db)):
    repo = SQLAlchemyPersonalRepository(db)
    caso_de_uso = ListarTrabajadores(repo)
    return caso_de_uso.ejecutar()

@router.get("/{id}", response_model=PersonalResponse)
def obtener_personal_por_id(id: int, db: Session = Depends(get_db)):
    repo = SQLAlchemyPersonalRepository(db)
    caso_de_uso = ObtenerTrabajadorPorId(repo)
    return caso_de_uso.ejecutar(id)