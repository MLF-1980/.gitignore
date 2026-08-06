import sys
from pathlib import Path

# Configurar la ruta raíz del proyecto (hsa/) de forma absoluta
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from src.infrastructure.persistence.database import SessionLocal
from src.infrastructure.persistence.repositories.sqlalchemy_iper_repository import SqlAlchemyIPERRepository

def test_insert_and_get_iper():
    db = SessionLocal()
    repo = SqlAlchemyIPERRepository(db)

    new_record = {
        "area_id": 1,
        "hazard_id": 1,
        "process_name": "Mantenimiento Preventivo",
        "task_description": "Revision de tableros electricos",
        "risk_level": "Alto",
        "control_measures": "Uso de EPP dieléctrico y bloqueo LOTO"
    }

    try:
        repo.add(new_record)
        print("✅ Registro IPER insertado correctamente.")

        records = repo.get_all()
        print(f"✅ Se encontraron {len(records)} registros en la matriz IPER.")
        for r in records:
            print(f"   - Proceso: {r.process_name}, Nivel de Riesgo: {r.risk_level}")
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_insert_and_get_iper()