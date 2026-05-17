from flask import Flask, render_template, request, redirect
from flask_wtf.csrf import CSRFProtect
# ADICIONA AS FUNÇÕES DE CRIPTOGRAFIA DE SENHA (Correção do Item 2)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# CONFIGURAÇÃO DA CHAVE SECRETA (Correção do Item 3)
app.config['SECRET_KEY'] = 'uma_chave_criptografica_muito_segura_e_longa_123'

# ATIVA A PROTEÇÃO CSRF GLOBALMENTE (Correção do Item 4)
csrf = CSRFProtect(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        
        # SIMULAÇÃO DE VALIDAÇÃO SEGURA (Item 2):
        # Em vez de testar texto limpo, o sistema usaria check_password_hash.
        # Aqui simulamos que a senha correta gravada no banco seria "123456" hashizada.
        senha_criptografada_banco = generate_password_hash("123456")
        
        if usuario == "admin" and check_password_hash(senha_criptografada_banco, senha):
            return redirect('/dashboard')
        else:
            return "Usuário ou senha incorretos!", 401
            
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # SEGURANÇA NA PRÁTICA (Item 2):
        # Antes de salvar no banco, transformamos a senha em um Hash seguro.
        senha_segura = generate_password_hash(senha)
        
        # Aqui os dados (nome, email, senha_segura) seriam salvos no banco.
        return redirect('/')
        
    return render_template('cadastro.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    # GARANTE MODO DE DEPURAÇÃO DESATIVADO EM PRODUÇÃO (Correção do Item 1)
    app.run(debug=False)