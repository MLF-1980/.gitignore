import json
from src.domain.entities import Trabajador, Nombre, MesesUsoEPP
from src.domain.repositories import TrabajadorRepository

class JSONTrabajadorRepository(TrabajadorRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def guardar(self, trabajador: Trabajador):
        # Convertimos el objeto de dominio a un diccionario simple
        data = {
            "id": trabajador.id_trabajador,
            "nombre": trabajador.nombre.valor,
            "meses_uso_epp": trabajador.meses_uso_epp.valor,
            "induccion_aprobada": trabajador.induccion_aprobada
        }
        
        # Escribimos en el archivo JSON
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"DEBUG: Trabajador {trabajador.id_trabajador} guardado exitosamente.")

    def obtener_por_id(self, id_trabajador: str) -> Trabajador:
        # Leemos el archivo JSON
        with open(self.file_path, "r") as f:
            data = json.load(f)
            
        # Reconstruimos el objeto respetando las reglas de los Value Objects
        return Trabajador(
            id_trabajador=data["id"],
            nombre=Nombre(data["nombre"]),
            meses_uso_epp=MesesUsoEPP(data["meses_uso_epp"]),
            induccion_aprobada=data["induccion_aprobada"]
        )