import pytest
from src.domain.entities import Trabajador, Nombre, MesesUsoEPP
from src.application.use_cases import RegistrarTrabajador

# Creamos un repositorio falso que no usa JSON, solo memoria
class FakeRepository:
    def __init__(self):
        self.db = []
    
    def guardar(self, trabajador):
        self.db.append(trabajador)

def test_registrar_trabajador():
    # 1. Preparar
    repo = FakeRepository()
    use_case = RegistrarTrabajador(repo)
    trabajador = Trabajador("1", Nombre("Test"), MesesUsoEPP(1), True)
    
    # 2. Actuar
    use_case.ejecutar(trabajador)
    
    # 3. Verificar (Assert)
    assert len(repo.db) == 1
    assert repo.db[0].id_trabajador == "1"