import os
from run import app
from app.database import db
from app.models.usuario_model import UsuarioModel
from app.models.ticket_model import TicketModel

def test_setup():
    print("Iniciando verificação do ambiente...")
    with app.app_context():
        # Verifica se as tabelas existem
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Tabelas no banco: {tables}")
        
        assert 'usuarios' in tables
        assert 'tickets' in tables
        
        # Verifica se o proprietário foi criado
        email_prop = os.getenv("PROPRIETARIO_EMAIL")
        prop = UsuarioModel.query.filter_by(email=email_prop).first()
        if prop:
            print(f"Proprietário {email_prop} encontrado com sucesso.")
        else:
            print("ERRO: Proprietário não encontrado.")
            exit(1)
            
    print("Ambiente configurado corretamente!")

if __name__ == "__main__":
    test_setup()
