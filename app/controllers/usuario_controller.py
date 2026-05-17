from flask import Blueprint, request, session, jsonify
from app.database import db
from app.models.usuario_model import UsuarioModel, UserRole
from app.utils.auth_utils import requer_roles

# Aqui está o nome exato que o __init__.py precisa encontrar!
usuario_blueprint = Blueprint('usuario', __name__)

@usuario_blueprint.route("/admin/atendentes", methods=["POST"])
@requer_roles(["ADMINISTRADOR"])
def cadastrar_atendente():
    dados = request.get_json() or request.form
    email = dados.get("email")
    senha = dados.get("senha")
    
    if not email or not senha:
        return jsonify({"erro": "Dados incompletos"}), 400

    # Cria o atendente associando-o ao Admin logado
    novo_atendente = UsuarioModel(
        email=email,
        role=UserRole.ATENDENTE,
        criado_por_id=session.get("user_id")
    )
    novo_atendente.set_senha(senha)
    
    db.session.add(novo_atendente)
    db.session.commit()
    
    return jsonify({"mensagem": "Atendente criado com sucesso vinculado à sua equipe"}), 201
