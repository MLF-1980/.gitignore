from typing import List, Optional
# Ajusta los imports según los nombres reales de tus entidades/repositorios en el proyecto
from src.domain.entities import Trabajador 
from src.domain.repositories import TrabajadorRepository
from src.domain.exceptions import UserNotFoundError  # Excepción personalizada que usaremos


class RegistrarTrabajador:
    def __init__(self, repo: TrabajadorRepository):
        self.repo = repo

    def ejecutar(self, trabajador: Trabajador):
        # Lógica de negocio para el registro
        return self.repo.guardar(trabajador)


class ListarTrabajadores:
    def __init__(self, repo: TrabajadorRepository):
        self.repo = repo

    def ejecutar(self) -> List[Trabajador]:
        # Lógica de negocio para listar todos los registros
        return self.repo.obtener_todos()


class ObtenerTrabajadorPorId:
    def __init__(self, repo: TrabajadorRepository):
        self.repo = repo

    def ejecutar(self, trabajador_id: int) -> Trabajador:
        # Lógica de negocio con validación de existencia
        trabajador = self.repo.obtener_por_id(trabajador_id)
        if not trabajador:
            raise UserNotFoundError(f"El trabajador con ID {trabajador_id} no fue encontrado.")
        return trabajador