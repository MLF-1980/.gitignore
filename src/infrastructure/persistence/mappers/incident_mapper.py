from src.domain.entities.incident import Incident
from src.infrastructure.persistence.models.incident_model import IncidentModel
class IncidentMapper:
    
    @staticmethod
    def to_domain(model: IncidentModel) -> Incident:
        if not model:
            return None
        return Incident(
            id=model.id,
            title=model.title,
            description=model.description,
            status=model.status,
            created_at=model.created_at
        )

    @staticmethod
    def to_persistence(incident: Incident) -> IncidentModel:
        if not incident:
            return None
        return IncidentModel(
            id=incident.id,
            title=incident.title,
            description=incident.description,
            status=incident.status,
            created_at=incident.created_at
        )