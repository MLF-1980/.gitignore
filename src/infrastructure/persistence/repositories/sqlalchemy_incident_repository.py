from sqlalchemy.orm import Session
from src.domain.entities.incident import Incident
from src.domain.repositories import IncidentRepositoryInterface
from src.infrastructure.persistence.models.incident_model import IncidentModel
from src.infrastructure.persistence.mappers.incident_mapper import IncidentMapper

class SqlAlchemyIncidentRepository(IncidentRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, incident_id: int) -> Incident | None:
        model = self._session.query(IncidentModel).filter(IncidentModel.id == incident_id).first()
        if not model:
            return None
        return IncidentMapper.to_domain(model)

    def get_all(self) -> list[Incident]:
        models = self._session.query(IncidentModel).all()
        return [IncidentMapper.to_domain(model) for model in models]

    def save(self, incident: Incident) -> None:
        model = IncidentMapper.to_persistence(incident)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)