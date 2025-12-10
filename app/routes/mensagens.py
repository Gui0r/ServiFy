"""
Rotas de gerenciamento de mensagens (Chat)
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Mensagem, Proposta
from app.utils.auth import get_current_user
from app.utils.validators import validate_required_fields

mensagens_bp = Blueprint('mensagens', __name__)

@mensagens_bp.route('/', methods=['POST'])
@jwt_required()
def criar_mensagem():
    """Envia uma mensagem em uma proposta"""
    try:
        current_user = get_current_user()
        data = request.get_json()
        
        required_fields = ['proposta_id', 'conteudo']
        is_valid, missing = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({
                "error": "Campos obrigatórios faltando",
                "missing": missing
            }), 400
        
        # Verifica se proposta existe
        proposta = Proposta.query.get_or_404(data['proposta_id'])
        
        # Verifica se usuário tem permissão (cliente ou profissional da proposta)
        tem_permissao = (
            proposta.solicitacao.cliente_id == current_user.id or
            proposta.profissional.usuario_id == current_user.id
        )
        
        if not tem_permissao:
            return jsonify({"error": "Acesso negado"}), 403
        
        # Verifica se proposta foi aceita (chat só funciona após aceitar)
        if proposta.status != 'aceita':
            return jsonify({"error": "Chat disponível apenas para propostas aceitas"}), 400
        
        # Cria mensagem
        nova_mensagem = Mensagem(
            proposta_id=data['proposta_id'],
            remetente_id=current_user.id,
            conteudo=data['conteudo']
        )
        
        db.session.add(nova_mensagem)
        db.session.commit()
        
        return jsonify({
            "message": "Mensagem enviada com sucesso",
            "mensagem": {
                "id": nova_mensagem.id,
                "conteudo": nova_mensagem.conteudo,
                "remetente": {
                    "id": current_user.id,
                    "nome": current_user.nome
                },
                "enviado_em": nova_mensagem.enviado_em.isoformat() if nova_mensagem.enviado_em else None
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao enviar mensagem: {str(e)}"}), 500

@mensagens_bp.route('/proposta/<int:proposta_id>', methods=['GET'])
@jwt_required()
def listar_mensagens(proposta_id):
    """Lista mensagens de uma proposta"""
    try:
        current_user = get_current_user()
        
        # Verifica se proposta existe
        proposta = Proposta.query.get_or_404(proposta_id)
        
        # Verifica permissão
        tem_permissao = (
            proposta.solicitacao.cliente_id == current_user.id or
            proposta.profissional.usuario_id == current_user.id
        )
        
        if not tem_permissao:
            return jsonify({"error": "Acesso negado"}), 403
        
        mensagens = Mensagem.query.filter_by(proposta_id=proposta_id)\
            .order_by(Mensagem.enviado_em.asc()).all()
        
        result = []
        for m in mensagens:
            mensagem_data = {
                "id": m.id,
                "conteudo": m.conteudo,
                "remetente": {
                    "id": m.remetente.id,
                    "nome": m.remetente.nome,
                    "tipo": m.remetente.tipo
                },
                "enviado_em": m.enviado_em.isoformat() if m.enviado_em else None
            }
            result.append(mensagem_data)
        
        return jsonify({
            "mensagens": result,
            "total": len(result)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao listar mensagens: {str(e)}"}), 500

