# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base
from manager.api.config import ConfigHandler
from typing import Generator

class Database:
    def __init__(self, config_handler: ConfigHandler):
        """Initialize the database connection based on the configuration."""
        self.config_handler = config_handler
        self.db_config = self.config_handler.get_database_config()
        self.DATABASE_URL = self._get_database_url(self.db_config)
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def _get_database_url(self, config):
        """Generate the database URL based on the configuration."""
        db_type = config.get('type', 'sqlite').lower()

        if db_type == 'sqlite':
            return f"sqlite:///{config.get('dbname', './xiaozhi.db')}"

        elif db_type == 'mysql':
            username = config.get('username', 'root')
            password = config.get('password', '')
            host = config.get('host', 'localhost')
            port = config.get('port', '3306')
            dbname = config.get('dbname', 'your_database_name')
            return f"mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}"

        elif db_type == 'postgresql':
            username = config.get('username', 'postgres')
            password = config.get('password', '')
            host = config.get('host', 'localhost')
            port = config.get('port', '5432')
            dbname = config.get('dbname', 'your_database_name')
            return f"postgresql://{username}:{password}@{host}:{port}/{dbname}"

        elif db_type == 'redis':
            return f"redis://{config.get('host', 'localhost')}:{config.get('port', '6379')}"

        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    def _create_engine(self):
        """Create the SQLAlchemy engine based on the database URL."""
        return create_engine(
            self.DATABASE_URL,
            connect_args={"check_same_thread": False} if self.db_config.get('type') == 'sqlite' else {}
        )

    def init_db(self):
        """Initialize the database by creating all tables."""
        Base.metadata.create_all(bind=self.engine)

    def get_db(self) -> Generator[Session, None, None]:
        """Provide a database session for dependency injection."""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


# Example usage:
# config_handler = ConfigHandler(session_manager=None)  # Assuming session_manager is not needed here
# db = Database(config_handler)
# db.init_db()  # Initialize the database
# session = next(db.get_db())  # Get a database session