from flask import Blueprint, render_template, session
from app.utils.auth_utils import requer_roles
from app.models.usuario_model import UsuarioModel, UserRole
from app.models.ticket_model import TicketModel

relatorio_blueprint = Blueprint('relatorio', __name__)

@relatorio_blueprint.route("/admin/relatorios")
@requer_roles(["PROPRIETARIO", "ADMINISTRADOR"])
def relatorios():
    # Coleta os dados reais direto do Banco de Dados SQLite
    total_atendentes = UsuarioModel.query.filter_by(role=UserRole.ATENDENTE).count()
    total_tickets = TicketModel.query.count()
    tickets_resolvidos = TicketModel.query.filter_by(status="RESOLVIDO").count()
    
    # Organiza em um dicionário estruturado
    dados_painel = {
        "total": total_tickets,
        "resolvidos": tickets_resolvidos,
        "equipe": total_atendentes
    }
    
    # Renderiza o arquivo HTML passando os dados coletados do banco
    return render_template("admin/relatorios.html", dados=dados_painel)
