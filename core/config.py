# app/core/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Camada Cash"

    SUPABASE_URL: str
    SUPABASE_KEY: str

    
    DATABASE_URL: str = ""
    
    
    GMAIL_USER: str
    GMAIL_PASSWORD: str
    
    
    JWT_SECRET: str
    
    ENV: str


    class Config:
        env_file = ".env"

settings = Settings()
