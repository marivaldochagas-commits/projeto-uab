from run import app, db
from models import Usuario

def test_criar_usuario():
    with app.app_context():
        # RED: Tentando salvar um usuário
        novo_user = Usuario(nome="Marivaldo", email="marivaldo@teste.com", senha="123")
        db.session.add(novo_user)
        db.session.commit()
        
        user_no_banco = Usuario.query.filter_by(email="marivaldo@teste.com").first()
        assert user_no_banco is not None
        assert user_no_banco.nome == "Marivaldo"
