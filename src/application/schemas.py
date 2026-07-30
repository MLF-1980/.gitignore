from typing import Optional
from pydantic import BaseModel


# Esquema para cuando el cliente CREA un registro (Entrada)
class PersonalCreate(BaseModel):
  nombre: str
  apellido: str
  dni: str
  cargo: str
  estado: Optional[str] = "Activo"


# Esquema para cuando la API DEVUELVE un registro (Salida)
class PersonalResponse(BaseModel):
  id: int
  nombre: str
  apellido: str
  dni: str
  cargo: str
  estado: str

  class Config:
    from_attributes = True  # Permite mapear modelos de SQLAlchemy a Pydantic