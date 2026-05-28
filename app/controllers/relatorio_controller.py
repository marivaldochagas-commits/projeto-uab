from flask import Blueprint, render_template, session, redirect, url_for
from app.models.usuario_model import UsuarioModel, UserRole
from app.models.ticket_model import TicketModel

relatorio_blueprint = Blueprint('relatorio', __name__)

@relatorio_blueprint.route("/admin/relatorios")
def relatorios():
    role_atual = session.get("usuario_role") or session.get("role")
    
    # Busca as contagens dos cards indicadores (que já estão funcionando!)
    total_atendentes = UsuarioModel.query.filter(UsuarioModel.role != "PROPRIETARIO").count()
    total_tickets = TicketModel.query.count()
    tickets_resolvidos = TicketModel.query.filter_by(status="RESOLVIDO").count()
    
    # CORREÇÃO AQUI: Busca todos os membros da equipe que não sejam o dono mestre
    # Isso evita travar por causa de maiúsculas/minúsculas do Enum no banco
    lista_equipe = UsuarioModel.query.filter(UsuarioModel.role != "PROPRIETARIO").all()
    
    dados_painel = {
        "total": total_tickets,
        "resolvidos": tickets_resolvidos,
        "equipe": total_atendentes
    }
    
    return render_template("admin/relatorios.html", dados=dados_painel, equipe=lista_equipe)