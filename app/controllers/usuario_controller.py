from flask import Blueprint, request, redirect, url_for, flash
from app.database import db
from app.models.usuario_model import UsuarioModel, UserRole

usuario_blueprint = Blueprint('usuario', __name__)

@usuario_blueprint.route("/admin/atendentes", methods=["POST"])
def cadastrar_atendente():
    # 1. Coleta os dados enviados pelo formulário HTML dentro da rota
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    
    # 2. Validação básica: garante que os campos essenciais não vieram vazios
    if not email or not senha:
        flash("Por favor, preencha todos os campos obrigatórios!", "danger")
        return redirect(url_for('relatorio.relatorios'))
        
    # 3. Verifica se o e-mail já existe no banco SQLite
    usuario_existente = UsuarioModel.query.filter_by(email=email).first()
    if usuario_existente:
        flash("Este e-mail já está cadastrado na equipe!", "danger")
        return redirect(url_for('relatorio.relatorios'))
        
    try:
        # 4. Cria o novo objeto usando as variáveis coletadas da requisição
        # Se o modelo não aceitar o campo 'nome', basta remover a linha abaixo
        novo_atendente = UsuarioModel(
            nome=nome if nome else email.split('@')[0], 
            email=email, 
            role=UserRole.ATENDENTE
        )
        
        # Criptografa a senha antes de salvar
        novo_atendente.set_senha(senha) 
        
        # 5. Grava fisicamente no banco de dados SQLite
        db.session.add(novo_atendente)
        db.session.commit()
        
        flash("Novo atendente cadastrado com sucesso!", "success")
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro detalhado no cadastro: {str(e)}")
        flash(f"Erro ao salvar o atendente no banco de dados: {str(e)}", "danger")
        
    # Redireciona de volta para atualizar a tabela na tela de relatórios
    return redirect(url_for('relatorio.relatorios'))