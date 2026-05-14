# Relatório de Mudanças - Aula 09 (Help Desk)

**Instituição:** IFTO - Pós-Graduação em Desenvolvimento de Sistemas Computacionais
**Disciplina:** Desenvolvimento Web
**Professor:** Fabio Silveira Vidal
**Grupo:** Marivaldo Lopes das Chagas, Gerson Carlos de Jesus, Daniel de Souza Costa, Roseni Alves Arruda Terra

---

## 1. Resumo da Etapa
Esta etapa marcou a transição do sistema de uma estrutura estática para uma aplicação baseada em dados dinâmicos. O foco principal foi a implementação da persistência de dados e a organização da lógica de negócio para o Help Desk.

## 2. Principais Alterações Realizadas

### A. Persistência com SQLite e SQLAlchemy
* Configuração do banco de dados relacional `projeto.db`.
* Implementação do mapeamento objeto-relacional (ORM) para evitar o uso de SQL puro, aumentando a segurança contra SQL Injection.

### B. Modelagem do Sistema de Atendimento
* **Modelo Usuario:** Definição de perfis (Cliente, Atendente, Administrador) para controle de permissões.
* **Modelo Ticket:** Criação da estrutura de chamados, incluindo campos para título, descrição, status e relacionamento com o usuário solicitante.

### C. Evolução das Rotas (Back-end)
* **Login Real:** A rota `/login` agora consulta o banco de dados para validar credenciais.
* **Fluxo de Dados:** Implementação de captura de dados via formulários (POST) e salvamento imediato no banco de dados.

## 3. Arquivos Atualizados
* `models.py`: Contém as definições das tabelas do banco de dados.
* `run.py`: Centralização das rotas e inicialização da aplicação com suporte ao Banco de Dados.
* `templates/`: Atualização dos formulários para garantir que os campos correspondam aos modelos do banco.

---
**Status da Entrega:** Concluída e enviada via controle de versão (Git).
