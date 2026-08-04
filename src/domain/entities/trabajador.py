from dataclasses import dataclass

@dataclass(frozen=True)
class Nombre:
    valor: str
    def __post_init__(self):
        if not self.valor or len(self.valor.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")

@dataclass(frozen=True)
class MesesUsoEPP:
    valor: int
    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("Los meses de uso no pueden ser negativos.")

class Trabajador:
    def __init__(self, id_trabajador: str, nombre, meses_uso_epp, induccion_aprobada: bool = False):
        self.id_trabajador = id_trabajador
        self.nombre = nombre
        self.meses_uso_epp = meses_uso_epp
        self.induccion_aprobada = induccion_aprobada

    def verificar_bloqueo_operativo(self) -> bool:
        return not self.induccion_aprobada

    def requiere_cambio_epp(self) -> bool:
        return self.meses_uso_epp.valor >= 6