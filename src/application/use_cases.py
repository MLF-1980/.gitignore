# src/application/use_cases.py
from src.domain.entities import Trabajador
from src.domain.repositories import TrabajadorRepository

class RegistrarTrabajador:
    def __init__(self, repo: TrabajadorRepository):
        # Aquí inyectamos el repositorio (contrato)
        self.repo = repo

    def ejecutar(self, trabajador: Trabajador):
        # Orquestamos la acción
        # Si hubiera que enviar un email o notificar, se haría aquí
        self.repo.guardar(trabajador)
        print(f"Caso de Uso: Trabajador {trabajador.id_trabajador} registrado con éxito.")