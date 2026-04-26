import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-default")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), os.getenv("DATABASE_PATH", "app/db/atendimento.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("DEBUG_MODE", "True") == "True"
    PROPRIETARIO_EMAIL = os.getenv("PROPRIETARIO_EMAIL")
    PROPRIETARIO_PASSWORD = os.getenv("PROPRIETARIO_PASSWORD")
