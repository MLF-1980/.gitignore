from src.domain.entities import Trabajador

def ejecutar_prueba():
    print("==============================================")
    print("   SISTEMA SAFECORE: VERIFICACIÓN DE DOMINIO  ")
    print("==============================================\n")

    # Simulamos un operario de Construcción con EPP al límite
    operario = Trabajador(
        id_trabajador=101,
        nombre="Juan Pérez",
        puesto="Soldador",
        rubro_empresa="Construccion",
        meses_uso_epp=3,
        induccion_aprobada=True
    )

    print(f"Evaluando estado de: {operario.nombre}")
    print(f" > ¿Requiere alerta de cambio de EPP?: {operario.evaluar_alerta_epp()}")
    print(f" > ¿Debe ser bloqueado el acceso?: {operario.verificar_bloqueo_operativo()}")
    print("==============================================")

if __name__ == "__main__":
    ejecutar_prueba()