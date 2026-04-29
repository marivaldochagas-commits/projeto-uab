from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    papel = db.Column(db.String(20), default='ATENDENTE')  # ADMIN ou ATENDENTE

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='ABERTO')  # ABERTO, EM_ANDAMENTO, RESOLVIDO
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento: liga o ticket ao usuário que o criou
    criado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    criado_por = db.relationship('Usuario', backref=db.backref('tickets', lazy=True))

    def __repr__(self):
        return f'<Ticket {self.titulo}>'
