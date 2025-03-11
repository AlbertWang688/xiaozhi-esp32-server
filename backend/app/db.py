
from sqlmodel import create_engine, Session, SQLModel
from backend.app.config import Settings
import os
from datetime import datetime

# Get the database URL from the settings
settings = Settings()
DATABASE_URL = settings.DATABASE_URL

if settings.DB_TYPE == "sqlite":
    import sqlite3
    # #注册sqlite的适配器和转换器
    # sqlite3.register_adapter(bool, int)
    # sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))
    # sqlite3.register_adapter(datetime, lambda v: v.isoformat())
    # sqlite3.register_converter("DATETIME", lambda v: datetime.fromisoformat(v.decode("utf-8")))

    # Check if the database file exists, if not, create it and the tables
    if not os.path.exists(settings.SQLITE_DB_FILE):
        print(f"Database file '{settings.SQLITE_DB_FILE}' not found. Creating new database and tables...")
        # engine = create_engine(DATABASE_URL, echo=True,connect_args={"detect_types": sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES})
        engine = create_engine(DATABASE_URL, echo=True)
        SQLModel.metadata.create_all(engine)
    else:
        # engine = create_engine(DATABASE_URL, echo=True,connect_args={"detect_types": sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES})
        engine = create_engine(DATABASE_URL, echo=True)
else:
    engine = create_engine(DATABASE_URL, echo=True)
def get_session():
    with Session(engine) as session:
        yield session