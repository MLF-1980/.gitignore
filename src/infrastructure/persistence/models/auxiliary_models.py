from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base  # Dos puntos para subir desde models/ hasta persistence/

class PlantModel(Base):
    __tablename__ = 'plants'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    region = Column(String(100), nullable=False)
    
    areas = relationship("AreaModel", back_populates="plant", cascade="all, delete-orphan")


class AreaModel(Base):
    __tablename__ = 'areas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    plant_id = Column(Integer, ForeignKey('plants.id'), nullable=False)
    
    plant = relationship("PlantModel", back_populates="areas")
    iper_records = relationship("IPERModel", back_populates="area")


class HazardCatalogModel(Base):
    __tablename__ = 'hazard_catalogs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True)
    description = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    
    iper_records = relationship("IPERModel", back_populates="hazard")