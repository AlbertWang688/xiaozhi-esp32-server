
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from fastapi import Depends
from backend.app.config import Settings
import os
from datetime import datetime


# Get the database URL from the settings
settings = Settings()
DATABASE_URL = settings.DATABASE_URL


if settings.DB_TYPE == "sqlite":
    # Check if the database file exists, if not, create it and the tables
    if not os.path.exists(settings.SQLITE_DB_FILE):
        print(f"Database file '{settings.SQLITE_DB_FILE}' not found. Creating new database and tables...")
        # engine = create_engine(DATABASE_URL, echo=True,connect_args={"detect_types": sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES})
        # engine = create_engine(DATABASE_URL, echo=True)
        engine = create_async_engine(DATABASE_URL)
        SQLModel.metadata.create_all(engine)
    else:
        # engine = create_engine(DATABASE_URL, echo=True,connect_args={"detect_types": sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES})
        engine = create_async_engine(DATABASE_URL, echo=True)
else:
    engine = create_async_engine(DATABASE_URL, echo=True)
async def get_session():
    async with AsyncSession(engine) as session:
        yield session