from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app.models.usuario_model import UsuarioModel

page_blueprint = Blueprint('pages', __name__)

@page_blueprint.route("/", methods=["GET", "POST"])
def index():
    # Se já estiver logado, manda direto para os chamados
    if "usuario_id" in session:
        return redirect(url_for('ticket.listar_ou_criar'))

    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        usuario = UsuarioModel.query.filter_by(email=email).first()

        # O bloco abaixo agora está DENTRO do if do POST
        if usuario and usuario.verificar_senha(senha):
            session["usuario_id"] = usuario.id
            session["usuario_email"] = usuario.email
            # Salvando a role de forma segura
            session["usuario_role"] = str(usuario.role.value).upper() if hasattr(usuario.role, 'value') else str(usuario.role).upper()

            return redirect(url_for('ticket.listar_ou_criar'))
        else:
            flash("E-mail ou senha incorretos!", "danger")
            return redirect(url_for('pages.index'))

    return render_template("login.html")

@page_blueprint.route("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada com sucesso.", "success")
    return redirect(url_for('pages.index'))

@page_blueprint.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    from app.database import db
    from werkzeug.security import generate_password_hash

    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario_existente = UsuarioModel.query.filter_by(email=email).first()
        if usuario_existente:
            flash("Este e-mail já está cadastrado!", "danger")
            return redirect(url_for('pages.cadastro'))

        try:
            novo_usuario = UsuarioModel(email=email)
            novo_usuario.senha_hash = generate_password_hash(senha)

            if hasattr(novo_usuario, 'nome'): novo_usuario.nome = nome
            elif hasattr(novo_usuario, 'name'): novo_usuario.name = nome

            if hasattr(novo_usuario, 'role'): novo_usuario.role = "CLIENTE"
            elif hasattr(novo_usuario, 'cargo'): novo_usuario.cargo = "CLIENTE"

            db.session.add(novo_usuario)
            db.session.commit()
            flash("Cadastro realizado com sucesso! Faça login.", "success")
            return redirect(url_for('pages.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao salvar: {str(e)}", "danger")
            return redirect(url_for('pages.cadastro'))

    return render_template("cadastro.html")