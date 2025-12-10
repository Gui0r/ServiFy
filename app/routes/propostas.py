"""
Rotas de gerenciamento de propostas
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Proposta, Solicitacao, Notificacao
from app.utils.auth import get_current_user, require_role
from app.utils.validators import validate_required_fields

propostas_bp = Blueprint('propostas', __name__)

@propostas_bp.route('/', methods=['POST'])
@jwt_required()
@require_role('profissional')
def criar_proposta(current_user):
    """Cria uma nova proposta para uma solicitação"""
    try:
        data = request.get_json()
        
        required_fields = ['solicitacao_id', 'valor', 'prazo_dias']
        is_valid, missing = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({
                "error": "Campos obrigatórios faltando",
                "missing": missing
            }), 400
        
        # Verifica se solicitação existe
        solicitacao = Solicitacao.query.get_or_404(data['solicitacao_id'])
        
        # Verifica se solicitação está aberta
        if solicitacao.status not in ['aberta', 'aguardando_propostas']:
            return jsonify({"error": "Solicitação não está aberta para propostas"}), 400
        
        # Verifica se profissional já enviou proposta
        profissional = current_user.profissional
        if not profissional:
            return jsonify({"error": "Perfil profissional não encontrado"}), 404
        
        proposta_existente = Proposta.query.filter_by(
            solicitacao_id=data['solicitacao_id'],
            profissional_id=profissional.id
        ).first()
        
        if proposta_existente:
            return jsonify({"error": "Você já enviou uma proposta para esta solicitação"}), 409
        
        # Cria proposta
        nova_proposta = Proposta(
            solicitacao_id=data['solicitacao_id'],
            profissional_id=profissional.id,
            valor=data['valor'],
            prazo_dias=data['prazo_dias'],
            mensagem=data.get('mensagem'),
            status='enviada'
        )
        
        db.session.add(nova_proposta)
        
        # Atualiza status da solicitação
        if solicitacao.status == 'aberta':
            solicitacao.status = 'aguardando_propostas'
        
        # Cria notificação para o cliente
        notificacao = Notificacao(
            usuario_id=solicitacao.cliente_id,
            titulo="Nova proposta recebida",
            mensagem=f"Você recebeu uma nova proposta para: {solicitacao.titulo}",
            tipo='sistema'
        )
        db.session.add(notificacao)
        
        db.session.commit()
        
        return jsonify({
            "message": "Proposta enviada com sucesso",
            "proposta": {
                "id": nova_proposta.id,
                "valor": float(nova_proposta.valor),
                "prazo_dias": nova_proposta.prazo_dias,
                "mensagem": nova_proposta.mensagem,
                "status": nova_proposta.status,
                "solicitacao_id": nova_proposta.solicitacao_id
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao criar proposta: {str(e)}"}), 500

@propostas_bp.route('/', methods=['GET'])
@jwt_required()
def listar_propostas():
    """Lista propostas (profissional vê suas, cliente vê recebidas)"""
    try:
        current_user = get_current_user()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status_filter = request.args.get('status')
        solicitacao_id = request.args.get('solicitacao_id', type=int)
        
        if current_user.tipo == 'profissional':
            profissional = current_user.profissional
            if not profissional:
                return jsonify({"error": "Perfil profissional não encontrado"}), 404
            
            query = Proposta.query.filter_by(profissional_id=profissional.id)
        elif current_user.tipo == 'cliente':
            # Cliente vê propostas de suas solicitações
            query = Proposta.query.join(Solicitacao).filter(
                Solicitacao.cliente_id == current_user.id
            )
        else:
            query = Proposta.query
        
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        if solicitacao_id:
            query = query.filter_by(solicitacao_id=solicitacao_id)
        
        propostas = query.order_by(Proposta.criado_em.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        result = []
        for p in propostas.items:
            proposta_data = {
                "id": p.id,
                "valor": float(p.valor),
                "prazo_dias": p.prazo_dias,
                "mensagem": p.mensagem,
                "status": p.status,
                "solicitacao": {
                    "id": p.solicitacao.id,
                    "titulo": p.solicitacao.titulo
                },
                "profissional": {
                    "id": p.profissional.id,
                    "nome": p.profissional.usuario.nome,
                    "nota_media": float(p.profissional.nota_media) if p.profissional.nota_media else 0
                },
                "criado_em": p.criado_em.isoformat() if p.criado_em else None
            }
            result.append(proposta_data)
        
        return jsonify({
            "propostas": result,
            "total": propostas.total,
            "page": page,
            "per_page": per_page,
            "pages": propostas.pages
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao listar propostas: {str(e)}"}), 500

@propostas_bp.route('/<int:proposta_id>', methods=['GET'])
@jwt_required()
def get_proposta(proposta_id):
    """Busca detalhes de uma proposta"""
    try:
        current_user = get_current_user()
        proposta = Proposta.query.get_or_404(proposta_id)
        
        # Verifica permissão
        if current_user.tipo == 'profissional':
            if proposta.profissional.usuario_id != current_user.id:
                return jsonify({"error": "Acesso negado"}), 403
        elif current_user.tipo == 'cliente':
            if proposta.solicitacao.cliente_id != current_user.id:
                return jsonify({"error": "Acesso negado"}), 403
        
        proposta_data = {
            "id": proposta.id,
            "valor": float(proposta.valor),
            "prazo_dias": proposta.prazo_dias,
            "mensagem": proposta.mensagem,
            "status": proposta.status,
            "solicitacao": {
                "id": proposta.solicitacao.id,
                "titulo": proposta.solicitacao.titulo,
                "descricao": proposta.solicitacao.descricao
            },
            "profissional": {
                "id": proposta.profissional.id,
                "nome": proposta.profissional.usuario.nome,
                "biografia": proposta.profissional.biografia,
                "nota_media": float(proposta.profissional.nota_media) if proposta.profissional.nota_media else 0
            },
            "criado_em": proposta.criado_em.isoformat() if proposta.criado_em else None
        }
        
        return jsonify(proposta_data), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar proposta: {str(e)}"}), 500

@propostas_bp.route('/<int:proposta_id>/aceitar', methods=['POST'])
@jwt_required()
@require_role('cliente')
def aceitar_proposta(current_user, proposta_id):
    """Aceita uma proposta (apenas o cliente dono da solicitação)"""
    try:
        proposta = Proposta.query.get_or_404(proposta_id)
        
        # Verifica se o cliente é dono da solicitação
        if proposta.solicitacao.cliente_id != current_user.id:
            return jsonify({"error": "Acesso negado"}), 403
        
        # Verifica se proposta está no status correto
        if proposta.status != 'enviada':
            return jsonify({"error": "Proposta não pode ser aceita neste status"}), 400
        
        # Verifica se solicitação está no status correto
        if proposta.solicitacao.status not in ['aberta', 'aguardando_propostas']:
            return jsonify({"error": "Solicitação não está aberta para aceitar propostas"}), 400
        
        # Atualiza proposta
        proposta.status = 'aceita'
        
        # Atualiza solicitação
        solicitacao = proposta.solicitacao
        solicitacao.status = 'proposta_aceita'
        
        # Rejeita outras propostas da mesma solicitação
        outras_propostas = Proposta.query.filter(
            Proposta.solicitacao_id == solicitacao.id,
            Proposta.id != proposta_id,
            Proposta.status == 'enviada'
        ).all()
        
        for p in outras_propostas:
            p.status = 'recusada'
        
        # Cria notificações
        notificacao_cliente = Notificacao(
            usuario_id=current_user.id,
            titulo="Proposta aceita",
            mensagem=f"Sua proposta para '{solicitacao.titulo}' foi aceita!",
            tipo='sistema'
        )
        db.session.add(notificacao_cliente)
        
        notificacao_profissional = Notificacao(
            usuario_id=proposta.profissional.usuario_id,
            titulo="Proposta aceita",
            mensagem=f"Sua proposta para '{solicitacao.titulo}' foi aceita pelo cliente!",
            tipo='sistema'
        )
        db.session.add(notificacao_profissional)
        
        db.session.commit()
        
        return jsonify({
            "message": "Proposta aceita com sucesso",
            "proposta": {
                "id": proposta.id,
                "status": proposta.status
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao aceitar proposta: {str(e)}"}), 500

@propostas_bp.route('/<int:proposta_id>/recusar', methods=['POST'])
@jwt_required()
@require_role('cliente')
def recusar_proposta(current_user, proposta_id):
    """Recusa uma proposta (apenas o cliente dono da solicitação)"""
    try:
        proposta = Proposta.query.get_or_404(proposta_id)
        
        if proposta.solicitacao.cliente_id != current_user.id:
            return jsonify({"error": "Acesso negado"}), 403
        
        if proposta.status != 'enviada':
            return jsonify({"error": "Proposta não pode ser recusada neste status"}), 400
        
        proposta.status = 'recusada'
        
        # Notifica o profissional
        notificacao = Notificacao(
            usuario_id=proposta.profissional.usuario_id,
            titulo="Proposta recusada",
            mensagem=f"Sua proposta para '{proposta.solicitacao.titulo}' foi recusada.",
            tipo='sistema'
        )
        db.session.add(notificacao)
        
        db.session.commit()
        
        return jsonify({"message": "Proposta recusada com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao recusar proposta: {str(e)}"}), 500

@propostas_bp.route('/<int:proposta_id>', methods=['PUT'])
@jwt_required()
@require_role('profissional')
def update_proposta(current_user, proposta_id):
    """Atualiza uma proposta (apenas o profissional dono, se ainda não foi aceita)"""
    try:
        proposta = Proposta.query.get_or_404(proposta_id)
        
        profissional = current_user.profissional
        if not profissional or proposta.profissional_id != profissional.id:
            return jsonify({"error": "Acesso negado"}), 403
        
        if proposta.status != 'enviada':
            return jsonify({"error": "Apenas propostas enviadas podem ser atualizadas"}), 400
        
        data = request.get_json()
        
        if 'valor' in data:
            proposta.valor = data['valor']
        if 'prazo_dias' in data:
            proposta.prazo_dias = data['prazo_dias']
        if 'mensagem' in data:
            proposta.mensagem = data['mensagem']
        
        db.session.commit()
        
        return jsonify({
            "message": "Proposta atualizada com sucesso",
            "proposta": {
                "id": proposta.id,
                "valor": float(proposta.valor),
                "prazo_dias": proposta.prazo_dias
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao atualizar proposta: {str(e)}"}), 500

