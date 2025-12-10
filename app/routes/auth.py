"""
Rotas de autenticação (Login e Registro)
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Usuario, Profissional
from app.utils.auth import hash_password, verify_password, create_token
from app.utils.validators import validate_email, validate_phone, validate_required_fields

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registro de novo usuário (Cliente ou Profissional)"""
    try:
        data = request.get_json()
        
        # Validação de campos obrigatórios
        required_fields = ['nome', 'email', 'senha', 'tipo']
        is_valid, missing = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({
                "error": "Campos obrigatórios faltando",
                "missing": missing
            }), 400
        
        # Validação de tipo
        if data['tipo'] not in ['cliente', 'profissional']:
            return jsonify({"error": "Tipo deve ser 'cliente' ou 'profissional'"}), 400
        
        # Validação de email
        if not validate_email(data['email']):
            return jsonify({"error": "Email inválido"}), 400
        
        # Verifica se email já existe
        if Usuario.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email já cadastrado"}), 409
        
        # Validação de telefone (se fornecido)
        if 'telefone' in data and data['telefone']:
            if not validate_phone(data['telefone']):
                return jsonify({"error": "Telefone inválido"}), 400
        
        # Cria novo usuário
        novo_usuario = Usuario(
            nome=data['nome'],
            email=data['email'],
            senha_hash=hash_password(data['senha']),
            telefone=data.get('telefone'),
            tipo=data['tipo']
        )
        
        db.session.add(novo_usuario)
        db.session.flush()  # Para obter o ID do usuário
        
        # Se for profissional, cria o perfil profissional
        if data['tipo'] == 'profissional':
            profissional = Profissional(
                usuario_id=novo_usuario.id,
                biografia=data.get('biografia'),
                raio_atendimento_km=data.get('raio_atendimento_km', 10)
            )
            db.session.add(profissional)
        
        db.session.commit()
        
        # Gera token JWT
        token = create_token(novo_usuario.id, novo_usuario.tipo)
        
        return jsonify({
            "message": "Usuário criado com sucesso",
            "token": token,
            "user": {
                "id": novo_usuario.id,
                "nome": novo_usuario.nome,
                "email": novo_usuario.email,
                "tipo": novo_usuario.tipo
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao criar usuário: {str(e)}"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login de usuário"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'senha' not in data:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400
        
        # Busca usuário
        usuario = Usuario.query.filter_by(email=data['email']).first()
        
        if not usuario or not verify_password(data['senha'], usuario.senha_hash):
            return jsonify({"error": "Email ou senha inválidos"}), 401
        
        # Gera token JWT
        token = create_token(usuario.id, usuario.tipo)
        
        response_data = {
            "message": "Login realizado com sucesso",
            "token": token,
            "user": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "tipo": usuario.tipo
            }
        }
        
        # Se for profissional, adiciona informações do perfil
        if usuario.tipo == 'profissional' and usuario.profissional:
            response_data["user"]["profissional"] = {
                "nota_media": float(usuario.profissional.nota_media) if usuario.profissional.nota_media else 0,
                "raio_atendimento_km": usuario.profissional.raio_atendimento_km
            }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao fazer login: {str(e)}"}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user_info():
    """Retorna informações do usuário autenticado"""
    try:
        from app.utils.auth import get_current_user
        usuario = get_current_user()
        
        if not usuario:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        user_data = {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "telefone": usuario.telefone,
            "tipo": usuario.tipo,
            "criado_em": usuario.criado_em.isoformat() if usuario.criado_em else None
        }
        
        # Se for profissional, adiciona informações do perfil
        if usuario.tipo == 'profissional' and usuario.profissional:
            user_data["profissional"] = {
                "id": usuario.profissional.id,
                "biografia": usuario.profissional.biografia,
                "nota_media": float(usuario.profissional.nota_media) if usuario.profissional.nota_media else 0,
                "raio_atendimento_km": usuario.profissional.raio_atendimento_km
            }
        
        return jsonify(user_data), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar informações: {str(e)}"}), 500

