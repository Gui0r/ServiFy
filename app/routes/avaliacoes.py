"""
Rotas de gerenciamento de avaliações
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Avaliacao, Solicitacao, Proposta
from app.utils.auth import get_current_user, require_role
from app.utils.validators import validate_required_fields

avaliacoes_bp = Blueprint('avaliacoes', __name__)

@avaliacoes_bp.route('/', methods=['POST'])
@jwt_required()
@require_role('cliente')
def criar_avaliacao(current_user):
    """Cria uma nova avaliação para um serviço concluído"""
    try:
        data = request.get_json()
        
        required_fields = ['solicitacao_id', 'nota']
        is_valid, missing = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({
                "error": "Campos obrigatórios faltando",
                "missing": missing
            }), 400
        
        # Valida nota
        nota = int(data['nota'])
        if nota < 1 or nota > 5:
            return jsonify({"error": "Nota deve estar entre 1 e 5"}), 400
        
        # Verifica se solicitação existe
        solicitacao = Solicitacao.query.get_or_404(data['solicitacao_id'])
        
        # Verifica se o cliente é dono da solicitação
        if solicitacao.cliente_id != current_user.id:
            return jsonify({"error": "Acesso negado"}), 403
        
        # Verifica se já existe avaliação
        if Avaliacao.query.filter_by(solicitacao_id=data['solicitacao_id']).first():
            return jsonify({"error": "Esta solicitação já foi avaliada"}), 409
        
        # Verifica se há proposta aceita
        proposta_aceita = Proposta.query.filter_by(
            solicitacao_id=data['solicitacao_id'],
            status='aceita'
        ).first()
        
        if not proposta_aceita:
            return jsonify({"error": "Não há proposta aceita para esta solicitação"}), 400
        
        # Cria avaliação
        nova_avaliacao = Avaliacao(
            solicitacao_id=data['solicitacao_id'],
            cliente_id=current_user.id,
            profissional_id=proposta_aceita.profissional_id,
            nota=nota,
            comentario=data.get('comentario')
        )
        
        db.session.add(nova_avaliacao)
        
        # Atualiza nota média do profissional
        profissional = proposta_aceita.profissional
        avaliacoes = Avaliacao.query.filter_by(profissional_id=profissional.id).all()
        if avaliacoes:
            nota_media = sum(a.nota for a in avaliacoes) / len(avaliacoes)
            profissional.nota_media = round(nota_media, 2)
        
        # Atualiza status da solicitação
        solicitacao.status = 'concluida'
        
        db.session.commit()
        
        return jsonify({
            "message": "Avaliação criada com sucesso",
            "avaliacao": {
                "id": nova_avaliacao.id,
                "nota": nova_avaliacao.nota,
                "comentario": nova_avaliacao.comentario,
                "solicitacao_id": nova_avaliacao.solicitacao_id
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao criar avaliação: {str(e)}"}), 500

@avaliacoes_bp.route('/', methods=['GET'])
@jwt_required()
def listar_avaliacoes():
    """Lista avaliações"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        profissional_id = request.args.get('profissional_id', type=int)
        
        query = Avaliacao.query
        
        if profissional_id:
            query = query.filter_by(profissional_id=profissional_id)
        
        avaliacoes = query.order_by(Avaliacao.criado_em.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        result = []
        for a in avaliacoes.items:
            avaliacao_data = {
                "id": a.id,
                "nota": a.nota,
                "comentario": a.comentario,
                "solicitacao": {
                    "id": a.solicitacao.id,
                    "titulo": a.solicitacao.titulo
                },
                "cliente": {
                    "id": a.cliente_avaliador.id,
                    "nome": a.cliente_avaliador.nome
                },
                "profissional": {
                    "id": a.profissional_avaliado.id,
                    "nome": a.profissional_avaliado.usuario.nome
                },
                "criado_em": a.criado_em.isoformat() if a.criado_em else None
            }
            result.append(avaliacao_data)
        
        return jsonify({
            "avaliacoes": result,
            "total": avaliacoes.total,
            "page": page,
            "per_page": per_page,
            "pages": avaliacoes.pages
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao listar avaliações: {str(e)}"}), 500

@avaliacoes_bp.route('/<int:avaliacao_id>', methods=['GET'])
@jwt_required()
def get_avaliacao(avaliacao_id):
    """Busca detalhes de uma avaliação"""
    try:
        avaliacao = Avaliacao.query.get_or_404(avaliacao_id)
        
        avaliacao_data = {
            "id": avaliacao.id,
            "nota": avaliacao.nota,
            "comentario": avaliacao.comentario,
            "solicitacao": {
                "id": avaliacao.solicitacao.id,
                "titulo": avaliacao.solicitacao.titulo
            },
            "cliente": {
                "id": avaliacao.cliente_avaliador.id,
                "nome": avaliacao.cliente_avaliador.nome
            },
            "profissional": {
                "id": avaliacao.profissional_avaliado.id,
                "nome": avaliacao.profissional_avaliado.usuario.nome
            },
            "criado_em": avaliacao.criado_em.isoformat() if avaliacao.criado_em else None
        }
        
        return jsonify(avaliacao_data), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar avaliação: {str(e)}"}), 500

