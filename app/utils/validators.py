"""
Utilitários de validação de dados
"""
import re
from flask import jsonify

def validate_email(email: str) -> bool:
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Valida formato de telefone brasileiro"""
    # Remove caracteres não numéricos
    phone_clean = re.sub(r'\D', '', phone)
    # Aceita telefones com 10 ou 11 dígitos (com DDD)
    return len(phone_clean) >= 10 and len(phone_clean) <= 11

def validate_required_fields(data: dict, required_fields: list) -> tuple:
    """
    Valida se todos os campos obrigatórios estão presentes
    Retorna (is_valid, missing_fields)
    """
    missing = [field for field in required_fields if field not in data or not data[field]]
    return (len(missing) == 0, missing)

def validate_request_json():
    """Decorator para validar se a requisição tem JSON válido"""
    def decorator(f):
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            if not request.is_json:
                return jsonify({"error": "Content-Type deve ser application/json"}), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator

