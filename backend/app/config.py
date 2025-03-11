from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # 数据库配置
    DB_TYPE: str = "sqlite"  # 可选 sqlite, mysql
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "xiaozhi"
    
    # SQLite 特定配置
    SQLITE_DB_FILE: str = "xiaozhi.db"
    
    # 其他通用配置
    API_PREFIX: str = "/api"
    DEBUG: bool = True
    
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    @property
    def DATABASE_URL(self) -> str:
        if self.DB_TYPE == "sqlite":
            return f"sqlite:///./{self.SQLITE_DB_FILE}"
        elif self.DB_TYPE == "mysql":
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        raise ValueError(f"Unsupported database type: {self.DB_TYPE}")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings() 