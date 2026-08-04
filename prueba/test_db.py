import sys
import os

# Agrega la raíz del proyecto al path de Python de forma automática
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.infrastructure.persistence.database import SessionLocal
from src.infrastructure.persistence.models.auxiliary_models import PlantModel, AreaModel, HazardCatalogModel
from src.infrastructure.persistence.models.iper_model import IPERModel

session = SessionLocal()

try:
    # 1. Crear una Planta y un Área auxiliar
    plant = PlantModel(name="Planta Principal", region="Norte")
    session.add(plant)
    session.commit()

    area = AreaModel(name="Línea de Producción 1", plant_id=plant.id)
    session.add(area)

    # 2. Crear un Peligro en el Catálogo auxiliar
    hazard = HazardCatalogModel(
        code="FIS-001", 
        description="Exposición a ruido excesivo", 
        category="Físico"
    )
    session.add(hazard)
    session.commit()

    # 3. Crear un registro en la Matriz IPER enlazado a las auxiliares
    iper_record = IPERModel(
        area_id=area.id,
        hazard_id=hazard.id,
        process_name="Operación de maquinaria pesada",
        task_description="Corte y moldeado de piezas metálicas",
        risk_level="Moderado",
        control_measures="Uso obligatorio de protectores auditivos de inserción."
    )
    session.add(iper_record)
    session.commit()

    print("¡Prueba exitosa! Los datos se guardaron y relacionaron correctamente en las tablas auxiliares y la matriz IPER.")

except Exception as e:
    session.rollback()
    print(f"Error durante la prueba de base de datos: {e}")

finally:
    session.close()