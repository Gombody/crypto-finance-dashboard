from sqlalchemy.engine import URL

from backend.config.settings import get_settings


def get_database_url() -> str:
    settings = get_settings()

    url = URL.create(
        drivername="postgresql+psycopg",
        username=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    )
    return str(url)