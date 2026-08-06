import os
import sys
from pathlib import Path
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from alembic.config import Config

# 1. Configuración del path absoluto para que Python reconozca 'src'
current_dir = Path(__file__).resolve().parent  # Directorio 'alembic'
# Sube los niveles necesarios hasta la raíz del proyecto que contiene 'src'
# (Asegúrate de ajustar el índice de 'parents' según la profundidad de tu carpeta)
sys.path.append(str(current_dir.parents[3])) 

# 2. Ahora sí, importa Base y los modelos de persistencia
from src.infrastructure.persistence.database import Base
from src.infrastructure.persistence.models.user_model import PersonalModel
from src.infrastructure.persistence.models.iper_model import IPERModel
from src.infrastructure.persistence.models.auxiliary_models import AreaModel, HazardCatalogModel

target_metadata = Base.metadata


# 1. Configuración del path absoluto para encontrar 'src'
current_dir = Path(__file__).resolve().parent  # Directorio 'alembic'
src_dir = current_dir.parents[2]  # Sube hasta la carpeta 'src'
sys.path.append(str(src_dir))

# 3. Carga directa y segura de la configuración desde 'alembic.ini' en la raíz (hsa)
root_dir = current_dir.parents[3]  # Carpeta raíz del proyecto 'hsa'
ini_path = root_dir / "alembic.ini"

if ini_path.exists():
    config = Config(str(ini_path))
else:
    config = context.config

if config and config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# 4. Inyección de la URL de base de datos (con fallback automático a SQLite local)
database_url = os.getenv("DATABASE_URL")

if not database_url:
    # Si no hay variable de entorno, apunta automáticamente a safecore.db en la raíz
    db_path = root_dir / "safecore.db"
    database_url = f"sqlite:///{db_path.as_posix()}"

# Sobrescribir la URL en la configuración de Alembic
config.set_main_option("sqlalchemy.url", database_url)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()