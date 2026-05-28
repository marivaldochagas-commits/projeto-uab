from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.database import db
from app.models.ticket_model import TicketModel, TicketStatus

ticket_blueprint = Blueprint('ticket', __name__)

@ticket_blueprint.route("/tickets", methods=["GET", "POST"])
def listar_ou_criar():
    usuario_id = session.get("usuario_id")
    usuario_email = session.get("usuario_email")
    usuario_role = session.get("usuario_role") or session.get("role") or session.get("cargo")
    
    if not usuario_id:
        return redirect(url_for('pages.index'))

    # 1. TRATAMENTO DO POST (Criar chamado)
    if request.method == "POST":
        assunto = request.form.get("assunto")
        if assunto:
            novo_ticket = TicketModel(
                cliente_id=usuario_id,
                status=TicketStatus.ABERTO,
                assunto=assunto
            )
            db.session.add(novo_ticket)
            db.session.commit()
        return redirect(url_for('ticket.listar_ou_criar'))

    # 2. TRATAMENTO DO GET (Exibir a tela correta)
    role_str = str(usuario_role).upper() if usuario_role else ""

    # SE FOR ADMIN, ATENDENTE OU PROPRIETÁRIO: Vai para a fila de gerenciamento total
    if "ADMIN" in role_str or "ATENDENTE" in role_str or "PROPRIETARIO" in role_str:
        todos_tickets = TicketModel.query.all()
        return render_template("admin/gerenciar_tickets.html", tickets=todos_tickets, role=usuario_role)
    
    # SE FOR CLIENTE: Vai para a tela azul e branca da Zil para abrir chamados
    else:
        meus_tickets = TicketModel.query.filter_by(cliente_id=usuario_id).all()
        return render_template("cliente/meus_tickets.html", tickets=meus_tickets, email=usuario_email)


@ticket_blueprint.route("/responder/<int:id>", methods=["POST"])
def responder_ticket(id):
    mensagem_solucao = request.form.get("solucao")
    if not mensagem_solucao:
        flash("O parecer técnico é obrigatório.", "danger")
        return redirect(url_for('ticket.listar_ou_criar'))

    ticket = TicketModel.query.get_or_404(id)
    try:
        ticket.status = TicketStatus.RESOLVIDO
        for coluna in ['solucao', 'resposta', 'observacao', 'historico']:
            if hasattr(ticket, coluna):
                setattr(ticket, coluna, mensagem_solucao)
                break
        db.session.commit()
        flash("Chamado resolvido com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao salvar: {str(e)}", "danger")
        
    return redirect(url_for('ticket.listar_ou_criar'))