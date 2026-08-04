from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.infrastructure.persistence.database import get_db
from src.infrastructure.persistence.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from src.application.use_cases import ListarTrabajadores, RegistrarTrabajador
from src.domain.entities.trabajador import Trabajador, Nombre, MesesUsoEPP

router = APIRouter(prefix="/personal", tags=["Personal"])

@router.get("/")
def listar_personal(db: Session = Depends(get_db)):
    repo = SqlAlchemyUserRepository(db)
    use_case = ListarTrabajadores(repo)
    return use_case.ejecutar()

@router.post("/")
def crear_personal(data: dict, db: Session = Depends(get_db)):
    repo = SqlAlchemyUserRepository(db)
    use_case = RegistrarTrabajador(repo)
    
    trabajador = Trabajador(
        id_trabajador=data.get("id_trabajador"),
        nombre=Nombre(data.get("nombre")),
        meses_uso_epp=MesesUsoEPP(data.get("meses_uso_epp")),
        induccion_aprobada=data.get("induccion_aprobada", False)
    )
    
    return use_case.ejecutar(trabajador)