from app.database import db
import enum
from werkzeug.security import generate_password_hash, check_password_hash

class UserRole(enum.Enum):
    PROPRIETARIO = "PROPRIETARIO"
    ADMINISTRADOR = "ADMINISTRADOR"
    ATENDENTE = "ATENDENTE"
    CLIENTE = "CLIENTE"

class UsuarioModel(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    criado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
        
    def verificar_senha(self, senha):
        # Garanta que todas as linhas abaixo tenham 8 espaços de recuo em relação ao início da margem
        if not self.senha_hash or not isinstance(self.senha_hash, str):
            return False
        try:
            return check_password_hash(self.senha_hash, senha)
        except Exception:
            return False