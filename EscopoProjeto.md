# ServiFy – Escopo Detalhado do Projeto: Marketplace de Serviços Locais

## 1. Resumo Executivo

O **ServiFy** é um projeto de desenvolvimento de um **Marketplace de Serviços Locais** inspirado no **"GetNinja"** com o objetivo de modernizar e centralizar a contratação de serviços autônomos. Inspirado em modelos de sucesso como o GetNinjas, a plataforma visa conectar clientes que necessitam de serviços (residenciais, técnicos ou gerais) a profissionais autônomos qualificados, promovendo um ambiente de negócios seguro, transparente e eficiente. O projeto engloba o desenvolvimento de uma **API robusta**, um **Painel Web** e um **Aplicativo Mobile nativo** para profissionais e clientes.

## 2. Visão Geral e Justificativa

### 2.1. Problema a Ser Resolvido

A contratação de serviços locais ainda é marcada por ineficiências e riscos, como a dependência de indicações informais, grupos de redes sociais ou classificados. Isso resulta em:
*   **Dificuldade de Encontrar Profissionais Qualificados:** A falta de um diretório centralizado e verificado.
*   **Falta de Confiança e Histórico:** Ausência de avaliações, histórico de trabalho e verificação de antecedentes.
*   **Processo de Orçamento Lento:** Clientes precisam contatar múltiplos profissionais individualmente.
*   **Desorganização:** Falta de centralização das solicitações e propostas.

### 2.2. Solução Proposta (ServiFy)

O ServiFy será a plataforma centralizada que resolve esses problemas através de:
*   **Conexão Inteligente:** Algoritmo de *matching* que conecta a solicitação do cliente aos profissionais mais relevantes por categoria e localização.
*   **Transparência e Confiança:** Perfis detalhados de profissionais com histórico de serviços, avaliações e selos de verificação.
*   **Agilidade:** Sistema de notificação e envio de propostas rápido e padronizado.
*   **Centralização:** Um único local para gerenciar solicitações, propostas, comunicação e pagamentos.

### 2.3. Público-Alvo

| Segmento | Descrição | Valor Agregado |
| :--- | :--- | :--- |
| **Clientes (Pessoas Físicas/Jurídicas)** | Indivíduos ou empresas que precisam contratar serviços de forma rápida, segura e com garantia de qualidade. | Praticidade, segurança, acesso a avaliações e histórico. |
| **Profissionais Autônomos** | Eletricistas, encanadores, marceneiros, diaristas, técnicos de TI, designers, etc., que buscam expandir sua base de clientes. | Novas oportunidades de negócio, visibilidade, gestão de reputação e histórico profissional. |
| **Pequenos Prestadores de Serviço** | Empresas ou MEIs que desejam uma plataforma para gerenciar a captação de *leads* e orçamentos. | Canal de aquisição de clientes de baixo custo e alta conversão. |

### 2.4. Categorias de Serviços (Exemplos Iniciais)

*   Serviços Residenciais (Eletricista, Encanador, Pintor, Diarista)
*   Serviços Técnicos (Técnico de Informática, Conserto de Eletrodomésticos)
*   Serviços Pessoais (Designer, Fotógrafo, Professor Particular)
*   Serviços Gerais (Fretes, Montador de Móveis, Jardineiro)

## 3. Escopo Funcional Detalhado (MVP)

O projeto será dividido em três módulos principais: **Cliente**, **Profissional** e **Comum/Administrativo**.

### 3.1. Módulo Cliente

| Funcionalidade | Descrição Detalhada |
| :--- | :--- |
| **Cadastro e Login** | Autenticação via e-mail/senha e redes sociais (Google, Facebook). |
| **Criação de Solicitação** | Formulário guiado para descrever o serviço, categoria, localização (CEP), prazo e anexar fotos/vídeos. |
| **Recebimento de Propostas** | Visualização de propostas recebidas, incluindo preço, prazo e perfil do profissional. |
| **Chat Integrado** | Canal de comunicação em tempo real (texto) para tirar dúvidas e negociar com o profissional selecionado. |
| **Avaliação e Feedback** | Sistema de avaliação (estrelas e comentário) após a conclusão do serviço. |
| **Gestão de Solicitações** | Acompanhamento do status (Pendente, Em Negociação, Contratado, Concluído, Cancelado). |

### 3.2. Módulo Profissional

| Funcionalidade | Descrição Detalhada |
| :--- | :--- |
| **Cadastro de Perfil** | Informações profissionais, portfólio, áreas de atuação, raio de atendimento e preço médio. |
| **Gestão de Serviços** | Definição das categorias e subcategorias de serviços que o profissional oferece. |
| **Recebimento de *Leads*** | Notificação em tempo real de novas solicitações relevantes (por categoria e localização). |
| **Envio de Propostas** | Formulário padronizado para enviar orçamento, prazo e mensagem personalizada ao cliente. |
| **Histórico de Serviços** | Registro de todos os serviços realizados, concluídos e cancelados. |
| **Gestão de Reputação** | Visualização das avaliações recebidas e cálculo da nota média. |

### 3.3. Módulo Comum e Administrativo

| Funcionalidade | Descrição Detalhada |
| :--- | :--- |
| **Autenticação Segura** | Implementação de JWT (JSON Web Tokens) e autenticação de dois fatores (2FA) opcional. |
| **Notificações** | Sistema de notificações *push* (Mobile) e e-mail (Web) para eventos críticos (nova proposta, chat, avaliação). |
| **Dashboard** | Painel de controle Web e Mobile com métricas e resumos de atividades para cada tipo de usuário. |
| **Mecanismo de Pagamento (Fase 2)** | Integração com *gateway* de pagamento (ex: Stripe, PagSeguro) para transações seguras e retenção de taxa de serviço. **(A ser implementado após o MVP)** |
| **Sistema de Disputas (Fase 2)** | Processo formal para mediação de conflitos entre cliente e profissional. **(A ser implementado após o MVP)** |
| **Painel de Administração** | CRUD (Create, Read, Update, Delete) para gerenciar usuários, categorias de serviço, moderação de conteúdo e relatórios básicos. |

## 4. Arquitetura e Tecnologia

A arquitetura será baseada em **Microsserviços** (inicialmente um Monolito Modular) com foco em escalabilidade e manutenção.

### 4.1. Stack Tecnológico

| Componente | Tecnologia | Justificativa |
| :--- | :--- | :--- |
| **API / Back-end** | **Python (Flask)** | Escolha por Flask devido à sua leveza, velocidade de desenvolvimento e adequação para APIs RESTful. |
| **Banco de Dados** | **MySQL** | Robustez, maturidade e adequação para dados relacionais (perfis, solicitações, propostas). |
| **Documentação** | **Swagger/OpenAPI** | Geração automática de documentação interativa para facilitar a integração e o desenvolvimento *front-end*. |
| **Aplicação Web** | **React** | Framework moderno e performático para a construção de interfaces ricas e responsivas. |
| **Aplicativo Mobile** | **Kotlin + Jetpack Compose** | Abordagem nativa para Android, garantindo alta performance e experiência de usuário otimizada. |
| **Comunicação** | **RESTful API** | Padrão de comunicação leve e amplamente adotado entre *front-end* e *back-end*. |

### 4.2. Estrutura de Dados (Modelo Entidade-Relacionamento - ER)

O modelo de dados inicial (MVP) será focado nas entidades centrais do marketplace:

| Entidade | Atributos Chave (Exemplos) | Relacionamentos |
| :--- | :--- | :--- |
| **Usuário** | `id`, `nome`, `email`, `tipo` (Cliente/Profissional), `localizacao`, `status` | 1:N com Solicitação (Cliente), 1:N com Proposta (Profissional), 1:N com Avaliação (Ambos) |
| **Serviço** | `id`, `nome_categoria`, `descricao` | 1:N com Solicitação |
| **Solicitação** | `id`, `titulo`, `descricao`, `localizacao`, `status`, `data_criacao` | N:1 com Usuário (Cliente), 1:N com Proposta |
| **Proposta** | `id`, `valor`, `prazo`, `mensagem`, `status` | N:1 com Usuário (Profissional), N:1 com Solicitação |
| **Avaliação** | `id`, `nota` (1-5), `comentario`, `data` | N:1 com Usuário (Cliente), N:1 com Usuário (Profissional) |

## 5. Requisitos Não Funcionais

| Categoria | Requisito | Detalhe |
| :--- | :--- | :--- |
| **Performance** | Tempo de Resposta | API deve responder em menos de 500ms para 90% das requisições. |
| **Segurança** | Proteção de Dados | Criptografia de senhas (hashing) e uso de HTTPS obrigatório. |
| **Usabilidade** | Design Responsivo | O Painel Web deve ser totalmente funcional em dispositivos móveis (além do app nativo). |
| **Manutenibilidade** | Padrões de Código | Uso de *linters* e testes unitários para garantir a qualidade do código. |

**Nota:** As funcionalidades de Pagamento e Sistema de Disputas são consideradas *Features* de Fase 2 e serão planejadas após a validação do do projeto.
