import json
import os
from typing import List, Optional
from sqlalchemy.orm import Session
from domain.exceptions import UserNotFoundError
from .models import PersonalModel


class JsonUserRepository:

  def __init__(self, file_path: str = "safeCore_db.json"):
    self.file_path = file_path
    self._ensure_file_exists()

  def _ensure_file_exists(self):
    if not os.path.exists(self.file_path):
      with open(self.file_path, "w", encoding="utf-8") as f:
        json.dump([], f)

  def _read_data(self) -> List[dict]:
    with open(self.file_path, "r", encoding="utf-8") as f:
      return json.load(f)

  def _write_data(self, data: List[dict]):
    with open(self.file_path, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=4, ensure_ascii=False)

  def save(self, user_dict: dict) -> dict:
    data = self._read_data()
    data.append(user_dict)
    self._write_data(data)
    return user_dict

  def get_by_id(self, user_id: str) -> Optional[dict]:
    data = self._read_data()
    for user in data:
      if user.get("id") == user_id:
        return user
    return None


class SQLAlchemyPersonalRepository:

  def __init__(self, db: Session):
    self.db = db

  def guardar(self, personal_data):
    db_item = PersonalModel(
        nombre=personal_data.nombre,
        apellido=personal_data.apellido,
        dni=personal_data.dni,
        cargo=personal_data.cargo,
        estado=getattr(personal_data, "estado", "Activo"),
    )
    self.db.add(db_item)
    self.db.commit()
    self.db.refresh(db_item)
    return db_item

  def obtener_todos(self):
    return self.db.query(PersonalModel).all()