from abc import ABC, abstractmethod
from src.domain.entities import Trabajador

class TrabajadorRepository(ABC):
    
    @abstractmethod
    def guardar(self, trabajador: Trabajador):
        """Obliga a cualquier repositorio a tener un método guardar"""
        pass

    @abstractmethod
    def obtener_por_id(self, id_trabajador: str) -> Trabajador:
        """Obliga a cualquier repositorio a saber buscar por ID"""
        pass