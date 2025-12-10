CREATE DATABASE IF NOT EXISTS servify CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE servify;

-- ============================================
-- 1. TABELA DE USUÁRIOS
-- ============================================
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    telefone VARCHAR(30),
    tipo ENUM('cliente', 'profissional', 'admin') NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 2. TABELA DE PROFISSIONAIS
-- ============================================
CREATE TABLE profissionais (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    biografia TEXT,
    nota_media DECIMAL(3,2) DEFAULT 0,
    raio_atendimento_km INT DEFAULT 10,
    
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- ============================================
-- 3. TABELAS DE CATEGORIAS
-- ============================================
CREATE TABLE categorias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE subcategorias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    categoria_id INT NOT NULL,
    nome VARCHAR(120) NOT NULL,

    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE
);

-- ============================================
-- 4. SERVIÇOS QUE O PROFISSIONAL OFERECE
-- ============================================
CREATE TABLE servicos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    profissional_id INT NOT NULL,
    subcategoria_id INT NOT NULL,
    descricao TEXT,
    preco_base DECIMAL(10,2),
    
    FOREIGN KEY (profissional_id) REFERENCES profissionais(id) ON DELETE CASCADE,
    FOREIGN KEY (subcategoria_id) REFERENCES subcategorias(id) ON DELETE RESTRICT
);

-- ============================================
-- 5. SOLICITAÇÕES FEITAS PELO CLIENTE
-- ============================================
CREATE TABLE solicitacoes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT NOT NULL,
    categoria_id INT NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    descricao TEXT,
    localizacao VARCHAR(255),
    status ENUM(
        'aberta',
        'aguardando_propostas',
        'proposta_aceita',
        'em_andamento',
        'concluida',
        'cancelada'
    ) DEFAULT 'aberta',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- ============================================
-- 6. PROPOSTAS DOS PROFISSIONAIS
-- ============================================
CREATE TABLE propostas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    solicitacao_id INT NOT NULL,
    profissional_id INT NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    prazo_dias INT NOT NULL,
    mensagem TEXT,
    status ENUM('enviada', 'aceita', 'recusada', 'cancelada') DEFAULT 'enviada',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (solicitacao_id) REFERENCES solicitacoes(id) ON DELETE CASCADE,
    FOREIGN KEY (profissional_id) REFERENCES profissionais(id) ON DELETE CASCADE
);

-- ============================================
-- 7. CHAT (MENSAGENS ENTRE CLIENTE E PROFISSIONAL)
-- ============================================
CREATE TABLE mensagens (
    id INT PRIMARY KEY AUTO_INCREMENT,
    proposta_id INT NOT NULL,
    remetente_id INT NOT NULL,
    conteudo TEXT NOT NULL,
    enviado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (proposta_id) REFERENCES propostas(id) ON DELETE CASCADE,
    FOREIGN KEY (remetente_id) REFERENCES usuarios(id)
);

-- ============================================
-- 8. AVALIAÇÕES
-- ============================================
CREATE TABLE avaliacoes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    solicitacao_id INT NOT NULL UNIQUE,
    cliente_id INT NOT NULL,
    profissional_id INT NOT NULL,
    nota TINYINT NOT NULL CHECK (nota BETWEEN 1 AND 5),
    comentario TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (solicitacao_id) REFERENCES solicitacoes(id),
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id),
    FOREIGN KEY (profissional_id) REFERENCES profissionais(id)
);

-- ============================================
-- 9. NOTIFICAÇÕES
-- ============================================
CREATE TABLE notificacoes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    mensagem TEXT NOT NULL,
    tipo ENUM('email', 'push', 'sistema') DEFAULT 'sistema',
    lida BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);
