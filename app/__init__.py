from flask import Flask
from config import Config
from app.database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    # Importa os controladores locais (Incluindo o novo de páginas)
    from app.controllers.usuario_controller import usuario_blueprint
    from app.controllers.relatorio_controller import relatorio_blueprint
    from app.controllers.page_controller import page_blueprint
    
    # Registra as Blueprints no app
    app.register_blueprint(usuario_blueprint)
    app.register_blueprint(relatorio_blueprint)
    app.register_blueprint(page_blueprint) # <--- Ativa a rota da página inicial
    
    return app
