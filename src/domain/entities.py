from dataclasses import dataclass

@dataclass
class Trabajador:
    """
    Entidad fundamental que representa a un operario dentro de la planta.
    Posee una identidad única a través de su 'id_trabajador'.
    """
    id_trabajador: int
    nombre: str
    puesto: str
    rubro_empresa: str          # Ejemplo: "Construccion" o "Otros"
    meses_uso_epp: int          # Invariante: Control de desgaste del equipamiento
    induccion_aprobada: bool    # Invariante: Control de acceso operativo
    
    def evaluar_alerta_epp(self) -> bool:
        """
        INVARIANTE 1: Ciclo de vida del EPP.
        Si el rubro es 'Construccion', el límite son 3 meses. Para otros, 6 meses.
        Retorna True si requiere cambio urgente.
        """
        if self.rubro_empresa.lower() == "construccion":
            return self.meses_uso_epp >= 3
        else:
            return self.meses_uso_epp >= 6

    def verificar_bloqueo_operativo(self) -> bool:
        """
        INVARIANTE 2: Bloqueo de tareas críticas.
        Si el operario no aprobó la inducción de ingreso, está inhabilitado.
        Retorna True si el trabajador debe ser violentado o bloqueado.
        """
        return not self.induccion_aprobada