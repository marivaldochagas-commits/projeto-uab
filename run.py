from app import create_app
from app.database import db
from app.models.usuario_model import UsuarioModel, UserRole
from config import Config

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Cria a estrutura do banco e todas as tabelas automaticamente
        db.create_all()
        
        # Injeção automática do Usuário Mestre (PROPRIETARIO) se não existir
        proprietario_existente = UsuarioModel.query.filter_by(email=Config.PROPRIETARIO_EMAIL).first()
        if not proprietario_existente:
            novo_proprietario = UsuarioModel(
                email=Config.PROPRIETARIO_EMAIL,
                role=UserRole.PROPRIETARIO
            )
            novo_proprietario.set_senha(Config.PROPRIETARIO_PASSWORD)
            db.session.add(novo_proprietario)
            db.session.commit()
            print(f"🚀 Usuário Mestre ({Config.PROPRIETARIO_EMAIL}) gerado com sucesso!")

    # Inicializa o servidor web seguindo a risca o modo seguro (debug=False via Config)
    app.run(host="0.0.0.0", port=5000)
