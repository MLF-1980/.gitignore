from src.domain.entities import Trabajador, Nombre, MesesUsoEPP
from src.infrastructure.repositories import JSONTrabajadorRepository

def ejecutar_prueba():
    print("==============================================")
    print("  SISTEMA SAFECORE: CONECTANDO DOMINIO -> INFRAESTRUCTURA  ")
    print("==============================================\n")

    # 1. Configuramos el repositorio (le decimos que use nuestro archivo JSON)
    repo = JSONTrabajadorRepository("safecore_db.json")

    # 2. Creamos nuestro trabajador
    operario = Trabajador(
        id_trabajador="101",
        nombre=Nombre("Juan Pérez"),
        meses_uso_epp=MesesUsoEPP(3),
        induccion_aprobada=True
    )

    # 3. Guardamos en el archivo (vía el repositorio)
    repo.guardar(operario)

    # 4. Prueba de fuego: Leemos desde el disco para verificar que realmente se guardó
    print("\n--- Verificando datos guardados en el disco ---")
    operario_recuperado = repo.obtener_por_id("101")

    # Evaluamos usando el objeto recuperado del disco
    print(f"Evaluando estado de: {operario_recuperado.nombre.valor}")
    print(f" > ¿Requiere alerta de cambio de EPP?: {operario_recuperado.requiere_cambio_epp()}")
    print(f" > ¿Debe ser bloqueado el acceso?: {operario_recuperado.verificar_bloqueo_operativo()}")
    print("==============================================")

if __name__ == "__main__":
    ejecutar_prueba()