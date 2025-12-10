"""
Rotas de gerenciamento de notificações
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Notificacao
from app.utils.auth import get_current_user

notificacoes_bp = Blueprint('notificacoes', __name__)

@notificacoes_bp.route('/', methods=['GET'])
@jwt_required()
def listar_notificacoes():
    """Lista notificações do usuário autenticado"""
    try:
        current_user = get_current_user()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        apenas_nao_lidas = request.args.get('apenas_nao_lidas', 'false').lower() == 'true'
        
        query = Notificacao.query.filter_by(usuario_id=current_user.id)
        
        if apenas_nao_lidas:
            query = query.filter_by(lida=False)
        
        notificacoes = query.order_by(Notificacao.criado_em.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        result = []
        for n in notificacoes.items:
            notificacao_data = {
                "id": n.id,
                "titulo": n.titulo,
                "mensagem": n.mensagem,
                "tipo": n.tipo,
                "lida": n.lida,
                "criado_em": n.criado_em.isoformat() if n.criado_em else None
            }
            result.append(notificacao_data)
        
        return jsonify({
            "notificacoes": result,
            "total": notificacoes.total,
            "nao_lidas": Notificacao.query.filter_by(
                usuario_id=current_user.id,
                lida=False
            ).count(),
            "page": page,
            "per_page": per_page,
            "pages": notificacoes.pages
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao listar notificações: {str(e)}"}), 500

@notificacoes_bp.route('/<int:notificacao_id>/marcar-lida', methods=['PUT'])
@jwt_required()
def marcar_como_lida(notificacao_id):
    """Marca uma notificação como lida"""
    try:
        current_user = get_current_user()
        notificacao = Notificacao.query.get_or_404(notificacao_id)
        
        if notificacao.usuario_id != current_user.id:
            return jsonify({"error": "Acesso negado"}), 403
        
        notificacao.lida = True
        db.session.commit()
        
        return jsonify({"message": "Notificação marcada como lida"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao marcar notificação: {str(e)}"}), 500

@notificacoes_bp.route('/marcar-todas-lidas', methods=['PUT'])
@jwt_required()
def marcar_todas_como_lidas():
    """Marca todas as notificações do usuário como lidas"""
    try:
        current_user = get_current_user()
        
        Notificacao.query.filter_by(
            usuario_id=current_user.id,
            lida=False
        ).update({"lida": True})
        
        db.session.commit()
        
        return jsonify({"message": "Todas as notificações foram marcadas como lidas"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao marcar notificações: {str(e)}"}), 500

@notificacoes_bp.route('/<int:notificacao_id>', methods=['DELETE'])
@jwt_required()
def deletar_notificacao(notificacao_id):
    """Deleta uma notificação"""
    try:
        current_user = get_current_user()
        notificacao = Notificacao.query.get_or_404(notificacao_id)
        
        if notificacao.usuario_id != current_user.id:
            return jsonify({"error": "Acesso negado"}), 403
        
        db.session.delete(notificacao)
        db.session.commit()
        
        return jsonify({"message": "Notificação deletada com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao deletar notificação: {str(e)}"}), 500

