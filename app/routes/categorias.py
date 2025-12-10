"""
Rotas de gerenciamento de categorias e subcategorias
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Categoria, Subcategoria
from app.utils.auth import get_current_user
from app.utils.validators import validate_required_fields

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/', methods=['GET'])
def listar_categorias():
    """Lista todas as categorias com suas subcategorias"""
    try:
        categorias = Categoria.query.all()
        
        result = []
        for cat in categorias:
            categoria_data = {
                "id": cat.id,
                "nome": cat.nome,
                "subcategorias": [{
                    "id": sub.id,
                    "nome": sub.nome
                } for sub in cat.subcategorias]
            }
            result.append(categoria_data)
        
        return jsonify({"categorias": result}), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao listar categorias: {str(e)}"}), 500

@categorias_bp.route('/<int:categoria_id>', methods=['GET'])
def get_categoria(categoria_id):
    """Busca uma categoria específica"""
    try:
        categoria = Categoria.query.get_or_404(categoria_id)
        
        categoria_data = {
            "id": categoria.id,
            "nome": categoria.nome,
            "subcategorias": [{
                "id": sub.id,
                "nome": sub.nome
            } for sub in categoria.subcategorias]
        }
        
        return jsonify(categoria_data), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar categoria: {str(e)}"}), 500

@categorias_bp.route('/', methods=['POST'])
@jwt_required()
def criar_categoria():
    """Cria uma nova categoria (requer autenticação)"""
    try:
        # Verifica se é admin
        current_user = get_current_user()
        if current_user.tipo != 'admin':
            return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json()
        
        required_fields = ['nome']
        is_valid, missing = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({
                "error": "Campos obrigatórios faltando",
                "missing": missing
            }), 400
        
        # Verifica se categoria já existe
        if Categoria.query.filter_by(nome=data['nome']).first():
            return jsonify({"error": "Categoria já existe"}), 409
        
        nova_categoria = Categoria(nome=data['nome'])
        db.session.add(nova_categoria)
        db.session.commit()
        
        return jsonify({
            "message": "Categoria criada com sucesso",
            "categoria": {
                "id": nova_categoria.id,
                "nome": nova_categoria.nome
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao criar categoria: {str(e)}"}), 500

@categorias_bp.route('/<int:categoria_id>/subcategorias', methods=['POST'])
@jwt_required()
def criar_subcategoria(categoria_id):
    """Cria uma nova subcategoria"""
    try:
        current_user = get_current_user()
        
        if current_user.tipo != 'admin':
            return jsonify({"error": "Acesso negado"}), 403
        
        categoria = Categoria.query.get_or_404(categoria_id)
        data = request.get_json()
        
        required_fields = ['nome']
        is_valid, missing = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({
                "error": "Campos obrigatórios faltando",
                "missing": missing
            }), 400
        
        nova_subcategoria = Subcategoria(
            categoria_id=categoria_id,
            nome=data['nome']
        )
        
        db.session.add(nova_subcategoria)
        db.session.commit()
        
        return jsonify({
            "message": "Subcategoria criada com sucesso",
            "subcategoria": {
                "id": nova_subcategoria.id,
                "nome": nova_subcategoria.nome,
                "categoria_id": categoria_id
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao criar subcategoria: {str(e)}"}), 500

