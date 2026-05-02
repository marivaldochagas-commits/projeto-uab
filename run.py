from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Usuario, Ticket
import os

app = Flask(__name__)
# Chave de segurança para permitir o uso de mensagens 'flash' e sessões
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui' 

# Configuração do caminho do banco de dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'projeto.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados dentro do aplicativo Flask
db.init_app(app)

# Rota da página inicial: mostra o formulário de login
@app.route('/')
def index():
    return render_template('login.html')

# Rota que processa os dados enviados pelo formulário de login


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':    # Precisa de 4 espaços (ou 1 Tab) aqui
            return "Sucesso Aula 07!"       # Precisa de 8 espaços (ou 2 Tabs) aqui
    return render_template('login.html')        # Precisa de 4 espaços aqui

    # Pega as informações que o usuário digitou
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    # Procura no banco de dados se esse usuário existe e a senha bate
    user = Usuario.query.filter_by(email=email, senha=senha).first()
    
    if user:
        # Se encontrou, exibe mensagem de boas-vindas
        return f"Bem-vindo, {user.nome}! Você está logado."
    else:
        # Se não encontrou, retorna erro de não autorizado (401)
        return "Login falhou. Verifique e-mail e senha.", 401

if __name__ == '__main__':
    # Inicia o servidor local para você testar no navegador
    app.run(debug=True)
