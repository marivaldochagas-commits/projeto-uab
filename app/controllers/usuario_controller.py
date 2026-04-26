from flask import Blueprint, request, session, jsonify
from app.database import db
from app.models.usuario_model import UsuarioModel, UserRole
from app.utils.auth_utils import requer_roles

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route("/admin/atendentes", methods=["POST"])
@requer_roles(["ADMINISTRADOR", "PROPRIETARIO"])
def criar_atendente():
    data = request.json
    email = data.get("email")
    senha = data.get("senha")
    
    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400
        
    novo = UsuarioModel(
        email=email,
        role=UserRole.ATENDENTE,
        criado_por_id=session.get("user_id")
    )
    novo.set_senha(senha)
    
    db.session.add(novo)
    db.session.commit()
    
    return jsonify({"mensagem": "Atendente criado com sucesso"}), 201
