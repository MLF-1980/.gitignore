from sqlalchemy import Column, Integer, String
from src.infrastructure.persistence.database import Base


class PersonalModel(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  nombre = Column(String, index=True)
  apellido = Column(String, index=True)
  dni = Column(String, unique=True, index=True)
  cargo = Column(String)
  estado = Column(String, default="Activo")
  