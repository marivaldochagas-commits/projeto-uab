from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Criamos a instância do banco de dados aqui
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuração do Banco de Dados (SQLite)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atendimento.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa o banco com as configurações do app
    db.init_app(app)
    
    # Registra as rotas
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
