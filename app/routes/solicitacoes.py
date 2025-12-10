"""
Rotas de gerenciamento de solicitações de serviço
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Solicitacao, Categoria, Usuario, Proposta
from app.utils.auth import get_current_user, require_role
from app.utils.validators import validate_required_fields

solicitacoes_bp = Blueprint('solicitacoes', __name__)

@solicitacoes_bp.route('/', methods=['POST'])
@jwt_required()
@require_role('cliente')
def criar_solicitacao(current_user):
    """Cria uma nova solicitação de serviço"""
    try:
        data = request.get_json()
        
        required_fields = ['titulo', 'categoria_id']
        is_valid, missing = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({
                "error": "Campos obrigatórios faltando",
                "missing": missing
            }), 400
        
        # Verifica se categoria existe
        categoria = Categoria.query.get(data['categoria_id'])
        if not categoria:
            return jsonify({"error": "Categoria não encontrada"}), 404
        
        nova_solicitacao = Solicitacao(
            cliente_id=current_user.id,
            categoria_id=data['categoria_id'],
            titulo=data['titulo'],
            descricao=data.get('descricao'),
            localizacao=data.get('localizacao'),
            status='aberta'
        )
        
        db.session.add(nova_solicitacao)
        db.session.commit()
        
        return jsonify({
            "message": "Solicitação criada com sucesso",
            "solicitacao": {
                "id": nova_solicitacao.id,
                "titulo": nova_solicitacao.titulo,
                "descricao": nova_solicitacao.descricao,
                "localizacao": nova_solicitacao.localizacao,
                "status": nova_solicitacao.status,
                "categoria": categoria.nome,
                "criado_em": nova_solicitacao.criado_em.isoformat() if nova_solicitacao.criado_em else None
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao criar solicitação: {str(e)}"}), 500

@solicitacoes_bp.route('/', methods=['GET'])
@jwt_required()
def listar_solicitacoes():
    """Lista solicitações (cliente vê suas próprias, profissional vê disponíveis)"""
    try:
        current_user = get_current_user()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status_filter = request.args.get('status')
        
        if current_user.tipo == 'cliente':
            # Cliente vê apenas suas solicitações
            query = Solicitacao.query.filter_by(cliente_id=current_user.id)
        elif current_user.tipo == 'profissional':
            # Profissional vê solicitações abertas ou aguardando propostas
            query = Solicitacao.query.filter(
                Solicitacao.status.in_(['aberta', 'aguardando_propostas'])
            )
        else:
            # Admin vê todas
            query = Solicitacao.query
        
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        solicitacoes = query.order_by(Solicitacao.criado_em.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        result = []
        for sol in solicitacoes.items:
            sol_data = {
                "id": sol.id,
                "titulo": sol.titulo,
                "descricao": sol.descricao,
                "localizacao": sol.localizacao,
                "status": sol.status,
                "categoria": sol.categoria.nome if sol.categoria else None,
                "criado_em": sol.criado_em.isoformat() if sol.criado_em else None
            }
            
            if current_user.tipo == 'cliente':
                sol_data["cliente"] = {
                    "id": sol.cliente.id,
                    "nome": sol.cliente.nome
                }
                sol_data["total_propostas"] = sol.propostas.count()
            else:
                sol_data["cliente"] = {
                    "id": sol.cliente.id,
                    "nome": sol.cliente.nome
                }
            
            result.append(sol_data)
        
        return jsonify({
            "solicitacoes": result,
            "total": solicitacoes.total,
            "page": page,
            "per_page": per_page,
            "pages": solicitacoes.pages
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao listar solicitações: {str(e)}"}), 500

@solicitacoes_bp.route('/<int:solicitacao_id>', methods=['GET'])
@jwt_required()
def get_solicitacao(solicitacao_id):
    """Busca detalhes de uma solicitação"""
    try:
        current_user = get_current_user()
        solicitacao = Solicitacao.query.get_or_404(solicitacao_id)
        
        # Cliente só pode ver suas próprias solicitações
        if current_user.tipo == 'cliente' and solicitacao.cliente_id != current_user.id:
            return jsonify({"error": "Acesso negado"}), 403
        
        sol_data = {
            "id": solicitacao.id,
            "titulo": solicitacao.titulo,
            "descricao": solicitacao.descricao,
            "localizacao": solicitacao.localizacao,
            "status": solicitacao.status,
            "categoria": {
                "id": solicitacao.categoria.id,
                "nome": solicitacao.categoria.nome
            } if solicitacao.categoria else None,
            "cliente": {
                "id": solicitacao.cliente.id,
                "nome": solicitacao.cliente.nome,
                "email": solicitacao.cliente.email
            },
            "criado_em": solicitacao.criado_em.isoformat() if solicitacao.criado_em else None
        }
        
        # Se for o cliente, inclui propostas recebidas
        if current_user.tipo == 'cliente' and solicitacao.cliente_id == current_user.id:
            propostas = solicitacao.propostas.all()
            sol_data["propostas"] = [{
                "id": p.id,
                "valor": float(p.valor),
                "prazo_dias": p.prazo_dias,
                "mensagem": p.mensagem,
                "status": p.status,
                "profissional": {
                    "id": p.profissional.id,
                    "nome": p.profissional.usuario.nome,
                    "nota_media": float(p.profissional.nota_media) if p.profissional.nota_media else 0
                },
                "criado_em": p.criado_em.isoformat() if p.criado_em else None
            } for p in propostas]
        
        return jsonify(sol_data), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar solicitação: {str(e)}"}), 500

@solicitacoes_bp.route('/<int:solicitacao_id>', methods=['PUT'])
@jwt_required()
@require_role('cliente')
def update_solicitacao(current_user, solicitacao_id):
    """Atualiza uma solicitação (apenas o cliente dono)"""
    try:
        solicitacao = Solicitacao.query.get_or_404(solicitacao_id)
        
        if solicitacao.cliente_id != current_user.id:
            return jsonify({"error": "Acesso negado"}), 403
        
        # Não permite atualizar se já tem proposta aceita
        if solicitacao.status in ['proposta_aceita', 'em_andamento', 'concluida']:
            return jsonify({"error": "Não é possível atualizar solicitação com status atual"}), 400
        
        data = request.get_json()
        
        if 'titulo' in data:
            solicitacao.titulo = data['titulo']
        if 'descricao' in data:
            solicitacao.descricao = data['descricao']
        if 'localizacao' in data:
            solicitacao.localizacao = data['localizacao']
        if 'categoria_id' in data:
            categoria = Categoria.query.get(data['categoria_id'])
            if not categoria:
                return jsonify({"error": "Categoria não encontrada"}), 404
            solicitacao.categoria_id = data['categoria_id']
        if 'status' in data:
            # Cliente pode cancelar ou reabrir
            if data['status'] in ['cancelada', 'aberta']:
                solicitacao.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            "message": "Solicitação atualizada com sucesso",
            "solicitacao": {
                "id": solicitacao.id,
                "titulo": solicitacao.titulo,
                "status": solicitacao.status
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao atualizar solicitação: {str(e)}"}), 500

@solicitacoes_bp.route('/<int:solicitacao_id>', methods=['DELETE'])
@jwt_required()
@require_role('cliente')
def delete_solicitacao(current_user, solicitacao_id):
    """Deleta uma solicitação (apenas o cliente dono, se não tiver propostas aceitas)"""
    try:
        solicitacao = Solicitacao.query.get_or_404(solicitacao_id)
        
        if solicitacao.cliente_id != current_user.id:
            return jsonify({"error": "Acesso negado"}), 403
        
        # Não permite deletar se já tem proposta aceita
        if solicitacao.status in ['proposta_aceita', 'em_andamento']:
            return jsonify({"error": "Não é possível deletar solicitação com proposta aceita"}), 400
        
        db.session.delete(solicitacao)
        db.session.commit()
        
        return jsonify({"message": "Solicitação deletada com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao deletar solicitação: {str(e)}"}), 500

