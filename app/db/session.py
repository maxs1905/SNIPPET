from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Подключение базы
database = Database(settings.DATABASE_URL)

# Async engine для Alembic и создания таблиц
engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

# Базовый класс моделей
Base = declarative_base()