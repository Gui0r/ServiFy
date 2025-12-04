from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Bem-vindo ao ServiFy API! O servidor está funcionando."}), 200
