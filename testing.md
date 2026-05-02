# Plano de Testes: Sistema de Atendimento (Tickets)
**Metodologia:** TDD First (Test-Driven Development)

## 1. Estratégia de Testes
O foco será a validação de cenários críticos e a prevenção de regressões em funcionalidades de segurança e persistência de dados.

## 2. Cenários de Teste por Funcionalidade

### 2.1 Gestão de Usuários (RBAC)
* **Caso de Teste 1:** Validar se um usuário com papel "ADMINISTRADOR" consegue criar apenas usuários do tipo "ATENDENTE".
    * **Prioridade:** Crítica.
    * **Resultado Esperado:** Sucesso ao criar atendente e erro 403 ao tentar criar outro administrador.
* **Caso de Teste 2:** Verificar se a hierarquia criado_por_id é gravada corretamente no banco de dados.

### 2.2 Ciclo de Vida do Ticket
* **Caso de Teste 3:** Validar a transição de status do ticket (ABERTO -> EM_ANDAMENTO -> RESOLVIDO).
    * **Dependência:** Uso de Mock para simular o ID do usuário logado.
* **Caso de Teste 4:** Garantir que um cliente visualize apenas os seus próprios tickets.

### 2.3 Relatórios Gerenciais
* **Caso de Teste 5:** Validar a agregação de dados no endpoint /admin/relatorios para garantir que o total de tickets resolvidos está correto.

## 3. Configuração do Ambiente de Testes
Para executar os testes, utilize o comando:
`pytest --verbose`

## Registro de Testes - Aula 07

### Teste de Interface Local
*   **Data:** 30/04/2026
*   **Descrição:** Verificação da renderização da tela de login.
*   **Resultado:** Sucesso. O servidor Flask carregou o template `login.html` corretamente em `http://127.0.0.1:5000`.

### Correções Realizadas
1.  **Ativação do Ambiente:** Foi necessário ativar o `venv` para carregar o módulo Flask.
2.  **Estrutura de Pastas:** O arquivo `login.html` foi movido para a pasta `/templates` para que o Jinja2 pudesse localizá-lo.