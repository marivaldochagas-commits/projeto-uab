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
    senha_hash = db.Column(db.String(128))
    role = db.Column(db.Enum(UserRole), nullable=False)
    criado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
        
    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
