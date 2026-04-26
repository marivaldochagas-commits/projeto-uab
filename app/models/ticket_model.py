from app.database import db
from datetime import datetime
import enum

class TicketStatus(enum.Enum):
    ABERTO = "ABERTO"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    RESOLVIDO = "RESOLVIDO"

class TicketModel(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    atendente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    assunto = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(TicketStatus), default=TicketStatus.ABERTO)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
