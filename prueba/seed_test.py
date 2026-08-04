from src.infrastructure.persistence.database import SessionLocal
from src.infrastructure.persistence.models.iper_model import IperMatrixModel

# Abrir sesión de base de datos
db = SessionLocal()

# Crear un registro de Matriz IPER para una obra simulada
sample_iper = IperMatrixModel(
    project_name="Obra Minera Norte",
    hazard="Manipulación de cargas pesadas en altura",
    risk="Caída de objetos y lesiones lumbares",
    control_measure="Uso obligatorio de EPP completo, grúa certificada y arnés de seguridad de doble vía",
    severity="Alto"
)

db.add(sample_iper)
db.commit()
db.refresh(sample_iper)

print(f"¡Matriz IPER creada con éxito! ID de registro: {sample_iper.id} para el proyecto: {sample_iper.project_name}")

# Consultar y mostrar el registro guardado (Simulando vista de auditoría)
result = db.query(IperMatrixModel).filter(IperMatrixModel.project_name == "Obra Minera Norte").first()
print("\n--- DATOS VISIBLES PARA EL AUDITOR ---")
print(f"Proyecto: {result.project_name}")
print(f"Peligro: {result.hazard}")
print(f"Riesgo: {result.risk}")
print(f"Medidas de Control: {result.control_measure}")
print(f"Criticidad: {result.severity}")

db.close()