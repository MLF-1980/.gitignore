from dataclasses import dataclass

# --- VALUE OBJECTS: Los porteros de tu sistema ---
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

# --- ENTIDAD DEL DOMINIO: Blindada ---
@dataclass(frozen=True)
class Trabajador:
    id_trabajador: str
    nombre: Nombre             # Usamos el Value Object
    meses_uso_epp: MesesUsoEPP # Usamos el Value Object
    induccion_aprobada: bool

    def verificar_bloqueo_operativo(self) -> bool:
        return not self.induccion_aprobada

    def requiere_cambio_epp(self) -> bool:
        return self.meses_uso_epp.valor >= 6

# --- INFRAESTRUCTURA: La capa técnica ---
class ServicioSeguridad:
    def __init__(self, repositorio_trabajadores):
        self.repo = repositorio_trabajadores

    def verificar_estado_seguridad(self, id_usuario: str) -> str:
        trabajador = self.repo.obtener_por_id(id_usuario)
        
        if trabajador.verificar_bloqueo_operativo():
            return "BLOQUEADO: Falta inducción."
        
        if trabajador.requiere_cambio_epp():
            return "ALERTA: EPP vencido."
            
        return "HABILITADO"

class RepositorioJSON:
    def obtener_por_id(self, id_usuario: str) -> Trabajador:
        # Aquí construimos los objetos. Si los datos fueran malos, fallaría aquí.
        return Trabajador(
            id_trabajador=id_usuario, 
            nombre=Nombre("Mauro"), 
            meses_uso_epp=MesesUsoEPP(7), 
            induccion_aprobada=True
        )