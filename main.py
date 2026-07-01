from src.domain.entities import Trabajador
# En main.py
from src.domain.entities import Trabajador, Nombre, MesesUsoEPP

def ejecutar_prueba():
    print("==============================================")
    print("   SISTEMA SAFECORE: VERIFICACIÓN DE DOMINIO  ")
    print("==============================================\n")

    # Simulamos un operario de Construcción con EPP al límite
    operario = Trabajador(
        id_trabajador=101,
        nombre=Nombre("Juan Pérez"),
            meses_uso_epp=MesesUsoEPP(3),
        induccion_aprobada=True
    )

    print(f"Evaluando estado de: {operario.nombre}")
    print(f" > ¿Requiere alerta de cambio de EPP?: {operario.requiere_cambio_epp()}")
    print(f" > ¿Debe ser bloqueado el acceso?: {operario.verificar_bloqueo_operativo()}")
    print("==============================================")

if __name__ == "__main__":
    ejecutar_prueba()