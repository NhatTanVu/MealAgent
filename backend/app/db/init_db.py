from sqlalchemy import create_engine, text
from app.core.config import settings

def get_db_name(database_url: str) -> str:
    return database_url.rsplit("/", 1)[-1]

def create_database_if_not_exists():
    db_name = get_db_name(settings.database_url)
    admin_engine = create_engine(
        settings.admin_database_url,
        isolation_level="AUTOCOMMIT"
    )

    with admin_engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": db_name}
        )

        exists = result.scalar() is not None

        if not exists:
            conn.execute(text(f'CREATE DATABASE "{db_name}"'))
            print(f"Database '{db_name}' created")
        else:
            print(f"Database '{db_name}' already exists")