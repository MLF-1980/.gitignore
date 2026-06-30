from dataclasses import dataclass
from typing import Optional

# 1. ENTIDAD DEL DOMINIO (Capa Central: I=0)
# Esta clase no sabe qué es un JSON, ni qué es una API, ni un Framework.
# Solo sabe las reglas de su propia existencia.
@dataclass(frozen=True)
class Trabajador:
    id_trabajador: str
    nombre: str
    meses_uso_epp: int
    induccion_aprobada: bool

    def verificar_bloqueo_operativo(self) -> bool:
        """
        Regla de negocio pura (Invariante).
        Si el operario no aprobó la inducción, está bloqueado.
        Esta lógica es inmutable y testable sin base de datos.
        """
        return not self.induccion_aprobada

    def requiere_cambio_epp(self) -> bool:
        """
        Invariante: Si supera los 6 meses, requiere cambio.
        """
        return self.meses_uso_epp >= 6

# 2. CAPA DE APLICACIÓN (Caso de Uso: El Orquestador)
# Esta capa le pide al "Repositorio" que traiga datos, 
# aplica la lógica del Dominio, y retorna el resultado.
class ServicioSeguridad:
    def __init__(self, repositorio_trabajadores):
        self.repo = repositorio_trabajadores

    def verificar_estado_seguridad(self, id_usuario: str) -> str:
        # El caso de uso orquesta el flujo, pero no calcula las reglas (eso lo hace el Dominio)
        trabajador = self.repo.obtener_por_id(id_usuario)
        
        if trabajador.verificar_bloqueo_operativo():
            return "BLOQUEADO: Falta inducción."
        
        if trabajador.requiere_cambio_epp():
            return "ALERTA: EPP vencido."
            
        return "HABILITADO"

# 3. CAPA DE INFRAESTRUCTURA (Detalle técnico: JSON)
# Aquí vive el acceso a 'safecore_db.json'. 
# Si mañana cambiamos a PostgreSQL, esta es la ÚNICA clase que cambia.
class RepositorioJSON:
    def obtener_por_id(self, id_usuario: str) -> Trabajador:
        # Simulamos la lectura de 'safecore_db.json'
        print(f"Leyendo de safecore_db.json para el ID: {id_usuario}")
        return Trabajador(id_usuario, "Mauro", 7, True)