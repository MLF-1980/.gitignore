# src/infrastructure/persistence/repositories/sqlalchemy_user_repository.py
from sqlalchemy.orm import Session  # type: ignore[reportMissingImports]
from ...models.iper_model import IPERModel

class SqlAlchemyIPERRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all(self):
        """Obtiene todos los registros de la Matriz IPER."""
        return self.db.query(IPERModel).all()

    def add(self, iper_data: dict) -> IPERModel:
        """Inserta un nuevo registro en la Matriz IPER."""
        db_record = IPERModel(
            area_id=iper_data["area_id"],
            hazard_id=iper_data["hazard_id"],
            process_name=iper_data["process_name"],
            task_description=iper_data["task_description"],
            risk_level=iper_data["risk_level"],
            control_measures=iper_data.get("control_measures")
        )
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return db_record