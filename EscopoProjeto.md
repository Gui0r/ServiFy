# ServiFy – Proposta de Projeto de Conclusão de Curso (TCC): Desenvolvimento de um Marketplace de Serviços Locais com Foco em Experiência do Usuário e Escalabilidade

## 1. Resumo

O **ServiFy** é um projeto de desenvolvimento de um **Marketplace de Serviços Locais** que visa modernizar e centralizar a contratação de serviços autônomos, inspirado em modelos de sucesso como o GetNinjas, mas com um foco estratégico na **Experiência do Usuário (UX)** e na **Escalabilidade Técnica**. A plataforma será projetada para conectar clientes que necessitam de serviços (residenciais, técnicos ou gerais) a profissionais autônomos qualificados, promovendo um ambiente de negócios seguro, transparente e eficiente.

O TCC não se limitará ao desenvolvimento técnico, mas também incluirá uma **Análise de Viabilidade Técnica e de Mercado** e uma **Proposta Metodológica de Desenvolvimento Ágil (Scrum/Kanban)**. O produto final do TCC será um **Produto Mínimo Viável (MVP)** funcional, composto por uma **API robusta**, um **Painel Web (para Clientes e Profissionais)** e um **Aplicativo Mobile Nativo (Android)**, acompanhado de um **Relatório Técnico-Científico** detalhado.

## 2. Visão Geral e Justificativa

### 2.1. Problema a Ser Resolvido (Aprofundamento)

A contratação de serviços locais no Brasil ainda é marcada por ineficiências e riscos, como a dependência de indicações informais e a falta de padronização. Isso gera:

*   **Assimetria de Informação:** Dificuldade do cliente em verificar a qualificação e o histórico do profissional.
*   **Fricção no Processo de Orçamento:** O cliente precisa contatar múltiplos profissionais, resultando em um processo lento e frustrante.
*   **Risco de Segurança:** Ausência de mecanismos de verificação de antecedentes e de mediação de conflitos.

### 2.2. Solução Proposta (ServiFy)

O ServiFy será a plataforma centralizada que resolve esses problemas através de:

*   **Algoritmo de *Matching* Otimizado:** Conexão inteligente baseada em categoria, localização e reputação do profissional.
*   **Mecanismos de Confiança:** Perfis detalhados, selos de verificação documental e histórico de avaliações.
*   **Fluxo de Proposta Simplificado:** Sistema padronizado de envio e aceitação de propostas.
*   **Centralização e Gestão:** Solicitações, propostas, comunicação via *chat* e, futuramente, pagamentos.

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

*   Abordagem Ágil (Scrum/Kanban).
*   Ferramentas: Trello ou Jira.
*   **Fases do MVP:**
    1. Configuração e Prototipagem
    2. Desenvolvimento do Back-end
    3. Desenvolvimento Web/Mobile
    4. Integração e Testes

---

## 7. Mapa de Telas (Wireframe de Navegação)

O mapa de telas a seguir define o fluxo de navegação principal para o MVP, dividindo as interfaces por perfil de usuário e plataforma (Web e Android).

### 7.1. Fluxo Comum (Web e Android)

| ID | Tela | Plataforma | Descrição | Próximas Telas |
| :--- | :--- | :--- | :--- | :--- |
| **T01** | Landing Page / Home | Web | Apresentação do ServiFy, busca de serviços, CTA para Cadastro/Login. | T02, T03, T04 |
| **T02** | Cadastro | Web/Android | Formulário de registro (Cliente ou Profissional). | T04, T05, T06 |
| **T03** | Login | Web/Android | Autenticação de usuário. | T05 (Cliente), T06 (Profissional) |
| **T04** | Busca de Serviços | Web/Android | Campo de busca por categoria/palavra-chave e localização. | T05.1 |

### 7.2. Fluxo Cliente

| ID | Tela | Plataforma | Descrição | Próximas Telas |
| :--- | :--- | :--- | :--- | :--- |
| **T05** | Dashboard Cliente | Web/Android | Resumo de solicitações ativas, propostas recebidas e status. | T05.1, T05.2, T05.3, T05.4 |
| **T05.1** | Criar Solicitação | Web/Android | Formulário detalhado (título, descrição, categoria, anexos). | T05 |
| **T05.2** | Detalhe da Solicitação | Web/Android | Status, lista de propostas recebidas. | T05.3, T05.4 |
| **T05.3** | Detalhe da Proposta | Web/Android | Visualização da proposta do profissional, perfil do profissional, botão Aceitar/Rejeitar. | T05.4 |
| **T05.4** | Chat Integrado | Web/Android | Comunicação em tempo real com o profissional após aceitar a proposta. | T05.5 |
| **T05.5** | Avaliação do Serviço | Web/Android | Formulário de nota (1-5) e comentário após conclusão. | T05 |

### 7.3. Fluxo Profissional

| ID | Tela | Plataforma | Descrição | Próximas Telas |
| :--- | :--- | :--- | :--- | :--- |
| **T06** | Dashboard Profissional | Web/Android | Resumo de leads (novas solicitações), propostas enviadas e reputação. | T06.1, T06.2, T06.3, T06.4 |
| **T06.1** | Gestão de Perfil | Web/Android | Edição de dados, portfólio, raio de atendimento e serviços oferecidos. | T06 |
| **T06.2** | Lista de Leads | Web/Android | Novas solicitações de serviço que correspondem ao perfil. | T06.3 |
| **T06.3** | Detalhe do Lead | Web/Android | Descrição completa da solicitação do cliente. Botão "Enviar Proposta". | T06.4 |
| **T06.4** | Envio de Proposta | Web/Android | Formulário para definir valor, prazo e mensagem personalizada. | T06 |
| **T06.5** | Histórico de Serviços | Web/Android | Lista de serviços concluídos e em andamento. | T06.6 |
| **T06.6** | Detalhe da Avaliação | Web/Android | Visualização das avaliações recebidas. | T06 |

---

## 8. Checklist Inicial de Desenvolvimento (MVP)

Este checklist serve como um guia para as primeiras tarefas a serem executadas, divididas por área técnica, alinhadas com a **Fase 1: Configuração e Prototipagem** e o início da **Fase 2: Desenvolvimento do Back-end** da metodologia ágil.

### 8.1. Back-end (API - Python/Flask + MySQL)

| Status | Tarefa | Detalhe |
| :--- | :--- | :--- |
| [ ] | **Configuração do Ambiente** | Instalar Python, Flask, MySQL e ferramentas de desenvolvimento (IDE). |
| [ ] | **Inicialização do Projeto** | Criar a estrutura básica do projeto Flask e configurar o ambiente virtual. |
| [ ] | **Configuração do Banco de Dados** | Instalar e configurar o MySQL. Definir e aplicar as migrações iniciais (tabelas Usuário, Serviço, Solicitação). |
| [ ] | **Autenticação (JWT)** | Implementar o módulo de registro e login de usuários com geração e validação de tokens JWT. |
| [ ] | **CRUD de Usuários** | Desenvolver endpoints básicos para criação, leitura, atualização e exclusão de perfis (Cliente e Profissional). |
| [ ] | **Documentação (Swagger)** | Configurar o Swagger/OpenAPI para documentar os primeiros endpoints de autenticação. |
| [ ] | **Containerização (Docker)** | Criar o `Dockerfile` e o `docker-compose.yml` para o Back-end e o Banco de Dados. |

### 8.2. Front-end Web (React)

| Status | Tarefa | Detalhe |
| :--- | :--- | :--- |
| [ ] | **Configuração do Projeto** | Inicializar o projeto React (CRA ou Vite) e configurar rotas básicas. |
| [ ] | **Design System Básico** | Definir paleta de cores, tipografia e componentes reutilizáveis (botões, inputs). |
| [ ] | **Página de Login/Cadastro** | Desenvolver as interfaces T02 e T03 e integrar com os endpoints de autenticação do Back-end. |
| [ ] | **Layout Responsivo** | Garantir que o layout base seja funcional em dispositivos móveis (Requisito Não Funcional de Usabilidade). |

### 8.3. Mobile Android (Kotlin + Jetpack Compose)

| Status | Tarefa | Detalhe |
| :--- | :--- | :--- |
| [ ] | **Configuração do Projeto** | Criar o projeto Android no Android Studio com Kotlin e Jetpack Compose. |
| [ ] | **Estrutura de Telas** | Implementar as telas T02 e T03 (Login/Cadastro) com navegação básica. |
| [ ] | **Integração com API** | Configurar uma biblioteca HTTP (ex: Retrofit) para comunicação com o Back-end. |
| [ ] | **Teste de Conexão** | Testar o fluxo de Login/Cadastro no emulador ou dispositivo físico. |

### 8.4. Documentação e Metodologia (TCC)

| Status | Tarefa | Detalhe |
| :--- | :--- | :--- |
| [ ] | **Estrutura do TCC** | Criar o documento base do TCC com os títulos das seções (Capítulos 1 a 6). |
| [ ] | **Referencial Teórico** | Iniciar a pesquisa bibliográfica sobre Marketplaces, UX/UI e Arquitetura de Microsserviços. |
| [ ] | **Ferramenta Ágil** | Configurar o Trello/Jira com as colunas (To Do, Doing, Done) e adicionar as tarefas deste checklist. |
| [ ] | **Revisão do Escopo** | Apresentar o escopo atualizado (incluindo o Mapa de Telas e o Checklist) ao orientador para validação. |
