from typing import List, Optional
# Ajusta los imports según los nombres reales de tus entidades/repositorios en el proyecto
from src.domain.entities.incident import Incident
from src.domain.repositories import IncidentRepositoryInterface
from src.domain.entities.incident import Trabajador 
from src.domain.repositories import UserRepository
from src.domain.exceptions import UserNotFoundError  # Excepción personalizada que usaremos


class RegistrarTrabajador:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def ejecutar(self, trabajador: Trabajador):
        # Lógica de negocio para el registro
        return self.repo.guardar(trabajador)


class ListarTrabajadores:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def ejecutar(self) -> List[Trabajador]:
        # Lógica de negocio para listar todos los registros
        return self.repo.obtener_todos()


class ObtenerTrabajadorPorId:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def ejecutar(self, trabajador_id: int) -> Trabajador:
        # Lógica de negocio con validación de existencia
        trabajador = self.repo.obtener_por_id(trabajador_id)
        if not trabajador:
            raise UserNotFoundError(f"El trabajador con ID {trabajador_id} no fue encontrado.")
        return trabajador

class RegistrarIncidente:
    def __init__(self, repo: IncidentRepositoryInterface):
        self.repo = repo

    def ejecutar(self, incident: Incident) -> Incident:
        # Lógica de negocio para registrar el incidente
        return self.repo.save(incident)


class ListarIncidentes:
    def __init__(self, repo: IncidentRepositoryInterface):
        self.repo = repo

    def ejecutar(self) -> List[Incident]:
        # Lógica de negocio para listar todos los incidentes
        return self.repo.get_all()


class ObtenerIncidentePorId:
    def __init__(self, repo: IncidentRepositoryInterface):
        self.repo = repo

    def ejecutar(self, incident_id: int) -> Incident:
        # Lógica de negocio con validación de existencia
        incident = self.repo.get_by_id(incident_id)
        if not incident:
            raise ValueError(f"El incidente con ID {incident_id} no fue encontrado.")
        return incident