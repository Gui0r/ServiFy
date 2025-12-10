import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.models import db # Importa o objeto db do seu arquivo models.py
from app.routes.main import main_bp # Importa o Blueprint de exemplo

def create_app():
    # 1. Cria a instância do Flask
    app = Flask(__name__)

    # 2. Carrega as configurações
    # A string de conexão será lida da variável de ambiente DATABASE_URL,
    # que é definida no seu docker-compose.yml
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:root_password_secure@localhost/servify')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuração de chave secreta (MUITO IMPORTANTE para segurança)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua_chave_secreta_padrao_muito_segura')
    
    # Configuração JWT
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', app.config['SECRET_KEY'])
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Tokens não expiram (pode ajustar depois)

    # 3. Inicializa extensões
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)  # Permite requisições CORS do frontend

    # 4. Registra os Blueprints (Rotas)
    app.register_blueprint(main_bp)
    
    # Registra todos os Blueprints
    from app.routes.auth import auth_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.solicitacoes import solicitacoes_bp
    from app.routes.propostas import propostas_bp
    from app.routes.avaliacoes import avaliacoes_bp
    from app.routes.mensagens import mensagens_bp
    from app.routes.notificacoes import notificacoes_bp
    from app.routes.categorias import categorias_bp
    from app.routes.profissionais import profissionais_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')
    app.register_blueprint(solicitacoes_bp, url_prefix='/api/solicitacoes')
    app.register_blueprint(propostas_bp, url_prefix='/api/propostas')
    app.register_blueprint(avaliacoes_bp, url_prefix='/api/avaliacoes')
    app.register_blueprint(mensagens_bp, url_prefix='/api/mensagens')
    app.register_blueprint(notificacoes_bp, url_prefix='/api/notificacoes')
    app.register_blueprint(categorias_bp, url_prefix='/api/categorias')
    app.register_blueprint(profissionais_bp, url_prefix='/api/profissionais')

    # 5. Cria as tabelas do banco de dados (opcional, mas útil para desenvolvimento)
    # Com o docker-compose, o banco de dados é criado automaticamente, mas 
    # esta linha garante que as tabelas sejam criadas se você rodar o app localmente
    # sem o Docker.
    with app.app_context():
        db.create_all()

    return app

# Ponto de execução principal
if __name__ == '__main__':
    app = create_app()
    # Roda o servidor Flask. O host '0.0.0.0' é necessário para rodar dentro do Docker.
    app.run(host='0.0.0.0', port=5000, debug=True)
