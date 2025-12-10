"""
Utilitários de autenticação e segurança
"""
import bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity
from functools import wraps
from flask import jsonify
from app.models import Usuario

def hash_password(password: str) -> str:
    """Gera hash da senha usando bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    """Verifica se a senha corresponde ao hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def create_token(user_id: int, tipo: str):
    """Cria token JWT para o usuário"""
    return create_access_token(
        identity=user_id,
        additional_claims={"tipo": tipo}
    )

def get_current_user():
    """Retorna o usuário atual baseado no token JWT"""
    user_id = get_jwt_identity()
    return Usuario.query.get(user_id)

def require_role(*allowed_roles):
    """Decorator para verificar se o usuário tem o tipo permitido"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_current_user()
            if not current_user:
                return jsonify({"error": "Usuário não autenticado"}), 401
            if current_user.tipo not in allowed_roles:
                return jsonify({"error": "Acesso negado"}), 403
            return f(current_user, *args, **kwargs)
        return decorated_function
    return decorator

