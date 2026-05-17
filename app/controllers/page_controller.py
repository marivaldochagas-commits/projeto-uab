from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app.models.usuario_model import UsuarioModel

page_blueprint = Blueprint('pages', __name__)

@page_blueprint.route("/", methods=["GET", "POST"])
def index():
    if "usuario_role" in session:
        return redirect(url_for('relatorio.relatorios'))
        
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        
        usuario = UsuarioModel.query.filter_by(email=email).first()
        
        if usuario and usuario.verificar_senha(senha):
            session["user_id"] = usuario.id
            session["usuario_role"] = usuario.role.value
            return redirect(url_for('relatorio.relatorios'))
        else:
            flash("E-mail ou senha incorretos!", "danger")
            
    return render_template("login.html")

@page_blueprint.route("/logout")
def logout():
    # Limpa toda a sessão ativa do navegador (Desloga o usuário)
    session.clear()
    flash("Sessão encerrada com sucesso.", "success")
    return redirect(url_for('pages.index'))
