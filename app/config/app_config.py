from pydantic_settings import BaseSettings , SettingsConfigDict
from functools import lru_cache

class app_config(BaseSettings):
    appname:str = "Expense-Tracker"
    appenv:str = "Development"
    database_url:str
    postgres_user:str
    postgres_pass:str
    postgres_db:str

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def getApp_config():
    return app_config