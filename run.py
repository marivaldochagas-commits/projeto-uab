from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# CONFIGURAÇÃO DA CHAVE SECRETA (Correção do Item 3)
app.config['SECRET_KEY'] = 'uma_chave_criptografica_muito_segura_e_longa_123'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect('/dashboard')  # Ao clicar em entrar, vai para o relatório
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=False)