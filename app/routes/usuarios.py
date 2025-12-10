"""
Rotas de gerenciamento de usuários
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Usuario
from app.utils.auth import get_current_user, require_role
from app.utils.validators import validate_email, validate_phone

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET'])
@jwt_required()
@require_role('admin')
def list_usuarios(current_user):
    """Lista todos os usuários (apenas admin)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        tipo_filter = request.args.get('tipo')
        
        query = Usuario.query
        
        if tipo_filter:
            query = query.filter_by(tipo=tipo_filter)
        
        usuarios = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            "usuarios": [{
                "id": u.id,
                "nome": u.nome,
                "email": u.email,
                "telefone": u.telefone,
                "tipo": u.tipo,
                "criado_em": u.criado_em.isoformat() if u.criado_em else None
            } for u in usuarios.items],
            "total": usuarios.total,
            "page": page,
            "per_page": per_page,
            "pages": usuarios.pages
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao listar usuários: {str(e)}"}), 500

@usuarios_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_usuario(user_id):
    """Busca um usuário específico"""
    try:
        current_user = get_current_user()
        
        # Usuário só pode ver seu próprio perfil, exceto admin
        if current_user.tipo != 'admin' and current_user.id != user_id:
            return jsonify({"error": "Acesso negado"}), 403
        
        usuario = Usuario.query.get_or_404(user_id)
        
        user_data = {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "telefone": usuario.telefone,
            "tipo": usuario.tipo,
            "criado_em": usuario.criado_em.isoformat() if usuario.criado_em else None
        }
        
        if usuario.tipo == 'profissional' and usuario.profissional:
            user_data["profissional"] = {
                "id": usuario.profissional.id,
                "biografia": usuario.profissional.biografia,
                "nota_media": float(usuario.profissional.nota_media) if usuario.profissional.nota_media else 0,
                "raio_atendimento_km": usuario.profissional.raio_atendimento_km
            }
        
        return jsonify(user_data), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar usuário: {str(e)}"}), 500

@usuarios_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_usuario(user_id):
    """Atualiza informações do usuário"""
    try:
        current_user = get_current_user()
        
        # Usuário só pode atualizar seu próprio perfil, exceto admin
        if current_user.tipo != 'admin' and current_user.id != user_id:
            return jsonify({"error": "Acesso negado"}), 403
        
        usuario = Usuario.query.get_or_404(user_id)
        data = request.get_json()
        
        if 'nome' in data:
            usuario.nome = data['nome']
        
        if 'email' in data:
            if not validate_email(data['email']):
                return jsonify({"error": "Email inválido"}), 400
            # Verifica se email já está em uso por outro usuário
            existing = Usuario.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                return jsonify({"error": "Email já está em uso"}), 409
            usuario.email = data['email']
        
        if 'telefone' in data:
            if data['telefone'] and not validate_phone(data['telefone']):
                return jsonify({"error": "Telefone inválido"}), 400
            usuario.telefone = data['telefone']
        
        if 'senha' in data and data['senha']:
            from app.utils.auth import hash_password
            usuario.senha_hash = hash_password(data['senha'])
        
        db.session.commit()
        
        return jsonify({
            "message": "Usuário atualizado com sucesso",
            "user": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "telefone": usuario.telefone
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao atualizar usuário: {str(e)}"}), 500

@usuarios_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@require_role('admin')
def delete_usuario(_, user_id):
    """Deleta um usuário (apenas admin)"""
    try:
        usuario = Usuario.query.get_or_404(user_id)
        
        # Não permite deletar a si mesmo
        current_user = get_current_user()
        if current_user.id == user_id:
            return jsonify({"error": "Não é possível deletar seu próprio usuário"}), 400
        
        db.session.delete(usuario)
        db.session.commit()
        
        return jsonify({"message": "Usuário deletado com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao deletar usuário: {str(e)}"}), 500

