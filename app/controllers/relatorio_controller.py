from flask import Blueprint, render_template, session
from app.database import db
from app.models.ticket_model import TicketModel, TicketStatus
from app.models.usuario_model import UsuarioModel
from app.utils.auth_utils import requer_roles

relatorio_bp = Blueprint('relatorio', __name__)

@relatorio_bp.route("/admin/relatorios", methods=["GET"])
@requer_roles(["ADMINISTRADOR", "PROPRIETARIO"])
def relatorios():
    total_geral = db.session.query(TicketModel).count()
    resolvidos = db.session.query(TicketModel).filter_by(status=TicketStatus.RESOLVIDO).count()
    
    tickets_equipe = 0
    usuario_logado_role = session.get("usuario_role")
    usuario_logado_id = session.get("user_id")
    
    if usuario_logado_role == "ADMINISTRADOR":
        tickets_equipe = db.session.query(TicketModel)\
            .join(UsuarioModel, TicketModel.atendente_id == UsuarioModel.id)\
            .filter(UsuarioModel.criado_por_id == usuario_logado_id).count()
            
    # Note: render_template will fail if the template file doesn't exist.
    # For now, I'll return JSON to allow testing without templates, 
    # or I could create a dummy template.
    return {
        "total": total_geral,
        "resolvidos": resolvidos,
        "equipe": tickets_equipe
    }
