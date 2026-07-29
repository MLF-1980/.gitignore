from sqlalchemy import Column, Integer, String
from .database import Base  # <-- Usar importación relativa con punto (.)


class PersonalModel(Base):
  __tablename__ = "personal"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  nombre = Column(String, index=True)
  apellido = Column(String, index=True)
  dni = Column(String, unique=True, index=True)
  cargo = Column(String)
  estado = Column(String, default="Activo")