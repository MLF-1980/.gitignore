from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.database import Base

from .auxiliary_models import AreaModel, HazardCatalogModel

class IPERModel(Base):
    __tablename__ = 'iper_records' # O el nombre de tabla que estés usando
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # --- LLAVES FORÁNEAS HACIA TABLAS AUXILIARES ---
    area_id = Column(Integer, ForeignKey('areas.id'), nullable=False)
    hazard_id = Column(Integer, ForeignKey('hazard_catalogs.id'), nullable=False)
    
    # --- CAMPOS PROPIOS DE LA MATRIZ IPER ---
    process_name = Column(String(150), nullable=False)  # Proceso / Actividad
    task_description = Column(Text, nullable=False)     # Rutinaria / No rutinaria
    
    # Evaluación de Riesgo (puedes adaptarlo a tu lógica de probabilidad x severidad)
    risk_level = Column(String(50), nullable=False)     # Ej: Trivial, Tolerable, Moderado, Importante, Intolerable
    control_measures = Column(Text, nullable=True)      # Medidas de control propuestas
    
    # --- RELACIONES ORM ---
    # Permite acceder a los datos de la zona y del catálogo directamente desde el objeto IPER
    area = relationship("AreaModel", back_populates="iper_records")
    hazard = relationship("HazardCatalogModel", back_populates="iper_records")