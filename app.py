import os
from flask import Flask
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

    # 3. Inicializa o SQLAlchemy
    db.init_app(app)

    # 4. Registra os Blueprints (Rotas)
    app.register_blueprint(main_bp)
    
    # Aqui você registraria outros Blueprints, como:
    # from app.routes.auth import auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    # from app.routes.users import users_bp
    # app.register_blueprint(users_bp, url_prefix='/users')

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
