from src.domain.entities import Trabajador, Nombre, MesesUsoEPP
from src.infrastructure.repositories import JSONTrabajadorRepository
from src.application.use_cases import RegistrarTrabajador

def ejecutar_prueba():
    print("=== EJECUTANDO CASO DE USO: REGISTRAR TRABAJADOR ===")
    
    # 1. Configuramos la infraestructura (el bibliotecario)
    repo = JSONTrabajadorRepository("safecore_db.json")
    
    # 2. Inyectamos la infraestructura en el Caso de Uso
    # (El caso de uso es el nuevo "Director de Orquesta")
    registro = RegistrarTrabajador(repo)

    # 3. Creamos el trabajador (nuestra Entidad de Dominio)
    nuevo_trabajador = Trabajador(
        id_trabajador="102",
        nombre=Nombre("Ana García"),
        meses_uso_epp=MesesUsoEPP(2),
        induccion_aprobada=True
    )

    # 4. El "main" ahora solo delega la acción al Caso de Uso
    registro.ejecutar(nuevo_trabajador)

if __name__ == "__main__":
    ejecutar_prueba()