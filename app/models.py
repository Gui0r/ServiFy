from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.schema import CheckConstraint

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(30))
    tipo = db.Column(ENUM('cliente', 'profissional', 'admin'), nullable=False)
    criado_em = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    # Relacionamentos
    profissional = db.relationship('Profissional', backref='usuario', uselist=False, cascade="all, delete-orphan")
    solicitacoes_feitas = db.relationship('Solicitacao', foreign_keys='Solicitacao.cliente_id', backref='cliente', lazy='dynamic', cascade="all, delete-orphan")
    mensagens_enviadas = db.relationship('Mensagem', foreign_keys='Mensagem.remetente_id', backref='remetente', lazy='dynamic')
    notificacoes = db.relationship('Notificacao', backref='usuario', lazy='dynamic', cascade="all, delete-orphan")
    avaliacoes_feitas = db.relationship('Avaliacao', foreign_keys='Avaliacao.cliente_id', backref='cliente_avaliador', lazy='dynamic')

    def __repr__(self):
        return f"<Usuario {self.nome} ({self.tipo})>"

class Profissional(db.Model):
    __tablename__ = 'profissionais'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    biografia = db.Column(db.Text)
    nota_media = db.Column(db.Numeric(3, 2), default=0)
    raio_atendimento_km = db.Column(db.Integer, default=10)

    # Relacionamentos
    servicos = db.relationship('Servico', backref='profissional', lazy='dynamic', cascade="all, delete-orphan")
    propostas_enviadas = db.relationship('Proposta', backref='profissional', lazy='dynamic', cascade="all, delete-orphan")
    avaliacoes_recebidas = db.relationship('Avaliacao', foreign_keys='Avaliacao.profissional_id', backref='profissional_avaliado', lazy='dynamic')

    def __repr__(self):
        return f"<Profissional {self.usuario.nome}>"

class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

    # Relacionamentos
    subcategorias = db.relationship('Subcategoria', backref='categoria', lazy='dynamic', cascade="all, delete-orphan")
    solicitacoes = db.relationship('Solicitacao', backref='categoria', lazy='dynamic')

    def __repr__(self):
        return f"<Categoria {self.nome}>"

class Subcategoria(db.Model):
    __tablename__ = 'subcategorias'
    
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id', ondelete='CASCADE'), nullable=False)
    nome = db.Column(db.String(120), nullable=False)

    # Relacionamentos
    servicos = db.relationship('Servico', backref='subcategoria', lazy='dynamic')

    def __repr__(self):
        return f"<Subcategoria {self.nome}>"

class Servico(db.Model):
    __tablename__ = 'servicos'
    
    id = db.Column(db.Integer, primary_key=True)
    profissional_id = db.Column(db.Integer, db.ForeignKey('profissionais.id', ondelete='CASCADE'), nullable=False)
    subcategoria_id = db.Column(db.Integer, db.ForeignKey('subcategorias.id', ondelete='RESTRICT'), nullable=False)
    descricao = db.Column(db.Text)
    preco_base = db.Column(db.Numeric(10, 2))

    def __repr__(self):
        return f"<Servico {self.subcategoria.nome} por {self.profissional.usuario.nome}>"

class Solicitacao(db.Model):
    __tablename__ = 'solicitacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    localizacao = db.Column(db.String(255))
    status = db.Column(ENUM(
        'aberta',
        'aguardando_propostas',
        'proposta_aceita',
        'em_andamento',
        'concluida',
        'cancelada'
    ), default='aberta')
    criado_em = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    # Relacionamentos
    propostas = db.relationship('Proposta', backref='solicitacao', lazy='dynamic', cascade="all, delete-orphan")
    avaliacao = db.relationship('Avaliacao', backref='solicitacao', uselist=False)

    def __repr__(self):
        return f"<Solicitacao {self.titulo} - Status: {self.status}>"

class Proposta(db.Model):
    __tablename__ = 'propostas'
    
    id = db.Column(db.Integer, primary_key=True)
    solicitacao_id = db.Column(db.Integer, db.ForeignKey('solicitacoes.id', ondelete='CASCADE'), nullable=False)
    profissional_id = db.Column(db.Integer, db.ForeignKey('profissionais.id', ondelete='CASCADE'), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    prazo_dias = db.Column(db.Integer, nullable=False)
    mensagem = db.Column(db.Text)
    status = db.Column(ENUM('enviada', 'aceita', 'recusada', 'cancelada'), default='enviada')
    criado_em = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    # Relacionamentos
    mensagens = db.relationship('Mensagem', backref='proposta', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Proposta para Solicitacao {self.solicitacao_id} - Valor: {self.valor}>"

class Mensagem(db.Model):
    __tablename__ = 'mensagens'
    
    id = db.Column(db.Integer, primary_key=True)
    proposta_id = db.Column(db.Integer, db.ForeignKey('propostas.id', ondelete='CASCADE'), nullable=False)
    remetente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    enviado_em = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Mensagem em Proposta {self.proposta_id} de {self.remetente_id}>"

class Avaliacao(db.Model):
    __tablename__ = 'avaliacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    solicitacao_id = db.Column(db.Integer, db.ForeignKey('solicitacoes.id'), nullable=False, unique=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    profissional_id = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=False)
    nota = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    criado_em = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    __table_args__ = (
        CheckConstraint('nota BETWEEN 1 AND 5', name='nota_check'),
    )

    def __repr__(self):
        return f"<Avaliacao Solicitacao {self.solicitacao_id} - Nota: {self.nota}>"

class Notificacao(db.Model):
    __tablename__ = 'notificacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    titulo = db.Column(db.String(150), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    tipo = db.Column(ENUM('email', 'push', 'sistema'), default='sistema')
    lida = db.Column(db.Boolean, default=False)
    criado_em = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Notificacao para {self.usuario_id} - {self.titulo}>"

# Exemplo de inicialização no seu app.py:
# from flask import Flask
# from models import db
# 
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@db_host/servify'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
# 
# with app.app_context():
#     db.create_all()
