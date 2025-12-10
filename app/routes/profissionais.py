"""
Rotas de gerenciamento de profissionais e serviços
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Profissional, Servico, Subcategoria
from app.utils.auth import get_current_user, require_role
from app.utils.validators import validate_required_fields

profissionais_bp = Blueprint('profissionais', __name__)

@profissionais_bp.route('/perfil', methods=['GET'])
@jwt_required()
@require_role('profissional')
def get_perfil_profissional(current_user):
    """Busca perfil do profissional autenticado"""
    try:
        profissional = current_user.profissional
        
        if not profissional:
            return jsonify({"error": "Perfil profissional não encontrado"}), 404
        
        # Busca serviços oferecidos
        servicos = Servico.query.filter_by(profissional_id=profissional.id).all()
        
        perfil_data = {
            "id": profissional.id,
            "biografia": profissional.biografia,
            "nota_media": float(profissional.nota_media) if profissional.nota_media else 0,
            "raio_atendimento_km": profissional.raio_atendimento_km,
            "usuario": {
                "id": current_user.id,
                "nome": current_user.nome,
                "email": current_user.email,
                "telefone": current_user.telefone
            },
            "servicos": [{
                "id": s.id,
                "subcategoria": {
                    "id": s.subcategoria.id,
                    "nome": s.subcategoria.nome,
                    "categoria": s.subcategoria.categoria.nome
                },
                "descricao": s.descricao,
                "preco_base": float(s.preco_base) if s.preco_base else None
            } for s in servicos]
        }
        
        return jsonify(perfil_data), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar perfil: {str(e)}"}), 500

@profissionais_bp.route('/perfil', methods=['PUT'])
@jwt_required()
@require_role('profissional')
def update_perfil_profissional(current_user):
    """Atualiza perfil do profissional"""
    try:
        profissional = current_user.profissional
        
        if not profissional:
            return jsonify({"error": "Perfil profissional não encontrado"}), 404
        
        data = request.get_json()
        
        if 'biografia' in data:
            profissional.biografia = data['biografia']
        
        if 'raio_atendimento_km' in data:
            raio = int(data['raio_atendimento_km'])
            if raio < 1:
                return jsonify({"error": "Raio de atendimento deve ser maior que 0"}), 400
            profissional.raio_atendimento_km = raio
        
        db.session.commit()
        
        return jsonify({
            "message": "Perfil atualizado com sucesso",
            "profissional": {
                "id": profissional.id,
                "biografia": profissional.biografia,
                "raio_atendimento_km": profissional.raio_atendimento_km
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao atualizar perfil: {str(e)}"}), 500

@profissionais_bp.route('/servicos', methods=['GET'])
@jwt_required()
@require_role('profissional')
def listar_servicos_profissional(current_user):
    """Lista serviços oferecidos pelo profissional"""
    try:
        profissional = current_user.profissional
        
        if not profissional:
            return jsonify({"error": "Perfil profissional não encontrado"}), 404
        
        servicos = Servico.query.filter_by(profissional_id=profissional.id).all()
        
        result = [{
            "id": s.id,
            "subcategoria": {
                "id": s.subcategoria.id,
                "nome": s.subcategoria.nome,
                "categoria": s.subcategoria.categoria.nome
            },
            "descricao": s.descricao,
            "preco_base": float(s.preco_base) if s.preco_base else None
        } for s in servicos]
        
        return jsonify({"servicos": result}), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao listar serviços: {str(e)}"}), 500

@profissionais_bp.route('/servicos', methods=['POST'])
@jwt_required()
@require_role('profissional')
def criar_servico(current_user):
    """Adiciona um serviço ao perfil do profissional"""
    try:
        profissional = current_user.profissional
        
        if not profissional:
            return jsonify({"error": "Perfil profissional não encontrado"}), 404
        
        data = request.get_json()
        
        required_fields = ['subcategoria_id']
        is_valid, missing = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({
                "error": "Campos obrigatórios faltando",
                "missing": missing
            }), 400
        
        # Verifica se subcategoria existe
        subcategoria = Subcategoria.query.get_or_404(data['subcategoria_id'])
        
        # Verifica se já oferece este serviço
        servico_existente = Servico.query.filter_by(
            profissional_id=profissional.id,
            subcategoria_id=data['subcategoria_id']
        ).first()
        
        if servico_existente:
            return jsonify({"error": "Você já oferece este serviço"}), 409
        
        novo_servico = Servico(
            profissional_id=profissional.id,
            subcategoria_id=data['subcategoria_id'],
            descricao=data.get('descricao'),
            preco_base=data.get('preco_base')
        )
        
        db.session.add(novo_servico)
        db.session.commit()
        
        return jsonify({
            "message": "Serviço adicionado com sucesso",
            "servico": {
                "id": novo_servico.id,
                "subcategoria": {
                    "id": subcategoria.id,
                    "nome": subcategoria.nome
                },
                "descricao": novo_servico.descricao,
                "preco_base": float(novo_servico.preco_base) if novo_servico.preco_base else None
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao criar serviço: {str(e)}"}), 500

@profissionais_bp.route('/servicos/<int:servico_id>', methods=['DELETE'])
@jwt_required()
@require_role('profissional')
def deletar_servico(current_user, servico_id):
    """Remove um serviço do perfil do profissional"""
    try:
        profissional = current_user.profissional
        
        if not profissional:
            return jsonify({"error": "Perfil profissional não encontrado"}), 404
        
        servico = Servico.query.get_or_404(servico_id)
        
        if servico.profissional_id != profissional.id:
            return jsonify({"error": "Acesso negado"}), 403
        
        db.session.delete(servico)
        db.session.commit()
        
        return jsonify({"message": "Serviço removido com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao deletar serviço: {str(e)}"}), 500

@profissionais_bp.route('/<int:profissional_id>', methods=['GET'])
def get_profissional_publico(profissional_id):
    """Busca informações públicas de um profissional"""
    try:
        profissional = Profissional.query.get_or_404(profissional_id)
        
        # Busca avaliações
        avaliacoes = profissional.avaliacoes_recebidas.order_by(
            profissional.avaliacoes_recebidas.property.mapper.class_.criado_em.desc()
        ).limit(5).all()
        
        profissional_data = {
            "id": profissional.id,
            "nome": profissional.usuario.nome,
            "biografia": profissional.biografia,
            "nota_media": float(profissional.nota_media) if profissional.nota_media else 0,
            "raio_atendimento_km": profissional.raio_atendimento_km,
            "servicos": [{
                "id": s.id,
                "subcategoria": {
                    "id": s.subcategoria.id,
                    "nome": s.subcategoria.nome,
                    "categoria": s.subcategoria.categoria.nome
                },
                "descricao": s.descricao,
                "preco_base": float(s.preco_base) if s.preco_base else None
            } for s in profissional.servicos],
            "avaliacoes_recentes": [{
                "nota": a.nota,
                "comentario": a.comentario,
                "cliente": a.cliente_avaliador.nome,
                "criado_em": a.criado_em.isoformat() if a.criado_em else None
            } for a in avaliacoes]
        }
        
        return jsonify(profissional_data), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar profissional: {str(e)}"}), 500

