from pydantic_settings import BaseSettings , SettingsConfigDict
from functools import lru_cache

class app_config(BaseSettings):
    app_name:str = "Expense-Tracker"
    app_env:str = "Development"
    database_url:str
    postgres_user:str
    postgres_password:str
    postgres_db:str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def getApp_config():
    return app_config()