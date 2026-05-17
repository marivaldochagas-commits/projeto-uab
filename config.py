import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-padrao-caso-nao-encontre")
    
    # Define o caminho do banco SQLite baseado na variável de ambiente
    db_path = os.getenv("DATABASE_PATH", "app/db/atendimento.db")
    # Garante que a pasta app/db exista
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.abspath(db_path)}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("DEBUG_MODE", "False").lower() in ("true", "1", "t")
    
    PROPRIETARIO_EMAIL = os.getenv("PROPRIETARIO_EMAIL")
    PROPRIETARIO_PASSWORD = os.getenv("PROPRIETARIO_PASSWORD")
