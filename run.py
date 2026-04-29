from flask import Flask
from models import db
import os

app = Flask(__name__)

# Configuração do Banco de Dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'projeto.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados no app
db.init_app(app)

@app.route('/')
def index():
    return "Sistema de Tickets Online"

if __name__ == '__main__':
    app.run(debug=True)
