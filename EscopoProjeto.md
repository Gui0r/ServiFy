# ServiFy – Proposta de Projeto de Conclusão de Curso (TCC): Desenvolvimento de um Marketplace de Serviços Locais com Foco em Experiência do Usuário e Escalabilidade

## 1. Resumo

O **ServiFy** é um projeto de desenvolvimento de um **Marketplace de Serviços Locais** que visa modernizar e centralizar a contratação de serviços autônomos, inspirado em modelos de sucesso como o GetNinjas, mas com um foco estratégico na **Experiência do Usuário (UX)** e na **Escalabilidade Técnica**. A plataforma será projetada para conectar clientes que necessitam de serviços (residenciais, técnicos ou gerais) a profissionais autônomos qualificados, promovendo um ambiente de negócios seguro, transparente e eficiente.

O TCC não se limitará ao desenvolvimento técnico, mas também incluirá uma **Análise de Viabilidade Técnica e de Mercado** e uma **Proposta Metodológica de Desenvolvimento Ágil (Scrum/Kanban)**. O produto final do TCC será um **Produto Mínimo Viável (MVP)** funcional, composto por uma **API robusta**, um **Painel Web (para Clientes e Profissionais)** e um **Aplicativo Mobile Nativo (Android)**, acompanhado de um **Relatório Técnico-Científico** detalhado.

## 2. Visão Geral e Justificativa

### 2.1. Problema a Ser Resolvido (Aprofundamento)

A contratação de serviços locais no Brasil ainda é marcada por ineficiências e riscos, como a dependência de indicações informais e a falta de padronização. Isso gera:

* **Assimetria de Informação:** Dificuldade do cliente em verificar a qualificação e o histórico do profissional.
* **Fricção no Processo de Orçamento:** O cliente precisa contatar múltiplos profissionais, resultando em um processo lento e frustrante.
* **Risco de Segurança:** Ausência de mecanismos de verificação de antecedentes e de mediação de conflitos.

### 2.2. Solução Proposta (ServiFy)

O ServiFy será a plataforma centralizada que resolve esses problemas através de:

* **Algoritmo de *Matching* Otimizado:** Conexão inteligente baseada em categoria, localização e reputação do profissional.
* **Mecanismos de Confiança:** Perfis detalhados, selos de verificação documental e histórico de avaliações.
* **Fluxo de Proposta Simplificado:** Sistema padronizado de envio e aceitação de propostas.
* **Centralização e Gestão:** Solicitações, propostas, comunicação via *chat* e, futuramente, pagamentos.

### 2.3. Público-Alvo e Análise de Mercado

| Segmento | Descrição | Valor Agregado |
| :--- | :--- | :--- |
| **Clientes (Pessoas Físicas/Jurídicas)** | Indivíduos ou empresas que buscam contratação rápida e segura. | Praticidade, segurança e avaliações. |
| **Profissionais Autônomos** | Profissionais que buscam aumentar sua base de clientes. | Oportunidades, visibilidade e reputação digital. |
| **Pequenos Prestadores de Serviço** | Empresas ou MEIs que desejam um canal de aquisição de *leads*. | Baixo custo e alta conversão. |

## 3. Escopo Funcional Detalhado (MVP)

O projeto será dividido em três módulos principais: **Cliente**, **Profissional** e **Comum/Administrativo**.

### 3.1. Módulo Cliente

| Funcionalidade | Descrição Detalhada |
| :--- | :--- |
| **Cadastro e Login** | Autenticação via e-mail/senha e redes sociais. |
| **Criação de Solicitação** | Descrição do serviço, categoria, localização e anexos. |
| **Recebimento de Propostas** | Visualização de propostas com preço, prazo e perfil do profissional. |
| **Chat Integrado** | Comunicação em tempo real. |
| **Avaliação e Feedback** | Nota e comentário após conclusão do serviço. |
| **Gestão de Solicitações** | Acompanhamento do status da solicitação. |

### 3.2. Módulo Profissional

| Funcionalidade | Descrição Detalhada |
| :--- | :--- |
| **Cadastro de Perfil** | Informações profissionais, portfólio e raio de atendimento. |
| **Gestão de Serviços** | Categorias e subcategorias oferecidas. |
| **Recebimento de Leads** | Notificação de novas solicitações. |
| **Envio de Propostas** | Envio de orçamento e prazo. |
| **Histórico de Serviços** | Registro de serviços realizados. |
| **Gestão de Reputação** | Avaliações recebidas e nota média. |

### 3.3. Módulo Comum e Administrativo

| Funcionalidade | Descrição Detalhada |
| :--- | :--- |
| **Autenticação Segura** | JWT e 2FA opcional. |
| **Notificações** | Push (mobile) e e-mail. |
| **Dashboard** | Métricas e resumos de atividades. |
| **Mecanismo de Pagamento (Fase 2)** | Integração com gateways. |
| **Sistema de Disputas (Fase 2)** | Mediação de conflitos. |
| **Painel de Administração** | CRUD de usuários, categorias e relatórios. |

## 4. Arquitetura e Tecnologia

A arquitetura será baseada em **Microsserviços** (iniciando como Monolito Modular).

### 4.1. Stack Tecnológico

| Componente | Tecnologia | Justificativa |
| :--- | :--- | :--- |
| **API / Back-end** | Python (Flask) | Leve e ideal para APIs. |
| **Banco de Dados** | MySQL | Robusto e relacional. |
| **Documentação** | Swagger/OpenAPI | Documentação interativa. |
| **Aplicação Web** | React | Front-end moderno. |
| **Aplicativo Mobile** | Kotlin + Jetpack Compose | Performance nativa Android. |
| **Comunicação** | REST + WebSockets | API e chat em tempo real. |
| **Infraestrutura** | Docker + GitHub Actions | Conteinerização e CI/CD. |

### 4.2. Estrutura de Dados (Modelo ER)

| Entidade | Atributos Chave | Relacionamentos |
| :--- | :--- | :--- |
| **Usuário** | id, nome, email, tipo, localização | 1:N com Solicitação, Proposta e Avaliação |
| **Serviço** | id, nome_categoria, descrição | 1:N com Solicitação |
| **Solicitação** | id, título, descrição, status, data | N:1 com Usuário; 1:N com Proposta |
| **Proposta** | id, valor, prazo, mensagem, status | N:1 com Usuário; N:1 com Solicitação |
| **Avaliação** | id, nota, comentário, data | N:1 com Cliente e Profissional |

## 5. Requisitos Não Funcionais

| Categoria | Requisito | Detalhe |
| :--- | :--- | :--- |
| **Performance** | Tempo de Resposta | API deve responder rápido. |
| **Segurança** | Proteção de Dados | Hashing e HTTPS. |
| **Usabilidade** | Design Responsivo | Web funcional em mobile. |
| **Manutenibilidade** | Padrões de Código | Testes unitários e linters. |
| **Escalabilidade** | Crescimento Horizontal | Arquitetura preparada para expansão. |

## 6. Metodologia do TCC

### 6.1. Estrutura do Trabalho Científico

1. Introdução  
2. Referencial Teórico  
3. Metodologia de Desenvolvimento  
4. Análise e Projeto  
5. Implementação e Resultados  
6. Conclusão  

### 6.2. Metodologia de Desenvolvimento

* Abordagem Ágil (Scrum/Kanban).  
* Ferramentas: Trello ou Jira.  
* **Fases do MVP:**  
  1. Configuração e Prototipagem  
  2. Desenvolvimento do Back-end  
  3. Desenvolvimento Web/Mobile  
  4. Integração e Testes  

