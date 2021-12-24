import os
from typing import Optional, Dict, Any

from pydantic import BaseSettings, validator, RedisDsn


class Settings(BaseSettings):
    """用于项目自定义配置"""

    DEBUG: bool
    SECRET_KEY: str
    MAX_CONTENT_LENGTH: int = 5 * 1024 * 1024 * 1024

    BASE_DIR: str = os.path.dirname(__file__)
    UPLOAD_DIR: str = "static/upload/"

    # 数据库配置
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str
    DB_PASS: str
    SQLALCHEMY_DATABASE_URI: Optional[str]

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        host = values.get("DB_HOST")
        port = values.get("DB_PORT")
        user = values.get("DB_USER")
        password = values.get("DB_PASS")
        db = values.get("DB_NAME")
        return f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'

    # redis配置
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_NAME: str
    REDIS_PASS: Optional[str]
    REDIS_MAX_CONNECTIONS: Optional[int] = 200
    REDIS_DSN: Optional[RedisDsn]

    @validator("REDIS_DSN", pre=True)
    def assemble_redis_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme='redis',
            host=values.get("REDIS_HOST"),
            port=f"{values.get('REDIS_PORT')}",
            password=values.get("REDIS_PASS"),
            path=f"/{values.get('REDIS_NAME')}"
        )

    # jwt配置
    TOKEN_EXPIRED_MINUTES: Optional[int] = 60

    class Config:
        case_sensitive = True
        env_file = os.path.join(os.path.dirname(__file__), ".env")
        env_file_encoding = 'utf-8'


settings = Settings()
