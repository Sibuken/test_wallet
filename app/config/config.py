from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataBase(BaseModel):
    name: str = "debug"
    user: str = "root"
    password: str = "debug"
    port: int = 3306
    host: str = "db"
    engine: str = "django.db.backends.mysql"
    conn_max_age: int = 0


class Config(BaseSettings):
    SECRET_KEY: str = "django-insecure-m2$&sk2$j!%423%d(t5zcj8xgq=-0a$o@7h6p7ymwiw64efe#a"
    DEBUG: bool = True
    ALLOWED_HOSTS: list[str] = ["*"]
    DATABASE: DataBase = DataBase()
    TIME_ZONE: str = "UTC"

    model_config = SettingsConfigDict(env_nested_delimiter="__")


env_config = Config()
