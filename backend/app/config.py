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

    #是否开启数据库异步模式
    ASYNC_MODE: bool = False
    
    # 其他通用配置
    API_PREFIX: str = "/api"
    DEBUG: bool = True
    
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings() 