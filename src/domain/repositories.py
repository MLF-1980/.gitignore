from abc import ABC, abstractmethod
from typing import List, Optional
# Ajusta la importación según dónde tengas tu clase Incident
from src.domain.entities.incident import Incident

class IncidentRepositoryInterface(ABC):
    
    @abstractmethod
    def save(self, incident: Incident) -> Incident:
        pass

    @abstractmethod
    def get_by_id(self, incident_id: int) -> Optional[Incident]:
        pass

    @abstractmethod
    def get_all(self) -> List[Incident]:
        pass

class UserRepository(ABC):
    @abstractmethod
    def get_by_dni(self, dni: str):
        pass

    @abstractmethod
    def save(self, user):
        pass