# Relatório de Inspeção de Segurança (Nível: Superficial)

**Projeto:** Sistema de Atendimento (Help Desk)  
**Data:** 15/05/2026  
**Instituição:** Instituto Federal do Tocantins (IFTO) / UAB - Campus Araguatins  
**Curso:** Pós-Graduação Lato Sensu em Desenvolvimento de Sistemas Computacionais  
**Disciplina:** Desenvolvimento Web  
**Aluno:** Marivaldo Lopes das Chagas  

---

## 📊 Resumo Executivo

Este relatório apresenta os resultados da inspeção de segurança em nível **Superficial** realizada no código-fonte e na estrutura inicial do projeto *Sistema de Atendimento*. A análise foi conduzida adotando as melhores práticas de desenvolvimento seguro de sistemas e utilizando como principal referencial teórico e metodológico o **OWASP Top 10 (Open Worldwide Application Security Project)**.

Através do mapeamento da raiz do projeto, do arquivo principal de rotas (`run.py`) e dos arquivos de interface (`login.html`, `cadastro.html`, `dashboard.html`), foram identificadas vulnerabilidades ligadas a configurações incorretas de ambiente, ausência de tratamento criptográfico nas credenciais e falta de proteção contra ataques automatizados de requisição. Por se tratar de um protótipo em estágio inicial, a aplicação exige intervenções estruturais antes de sua migração para um ambiente de produção real.

### 📈 Contagem de Achados por Severidade
* 🔴 **Crítica:** 0 achados
* 🟠 **Alta:** 2 achados
* 🟡 **Média:** 2 achados
* 🟢 **Baixa:** 1 achado

---

## 🚨 As 5 Ações Mais Urgentes (Plano de Mitigação)

1. **Desativar o Modo de Depuração (Debug Mode):** Desabilitar imediatamente o parâmetro `debug=True` no Flask para execução em ambientes externos, impedindo o vazamento de informações e execução de código remoto.
2. **Implementar Hashing de Senhas:** Substituir o tráfego e armazenamento simulado de credenciais em texto claro pela aplicação de algoritmos de dispersão criptográfica (como o `Werkzeug` ou `bcrypt`).
3. **Gerar e Configurar Chave Secreta (`SECRET_KEY`):** Definir uma chave secreta forte para a aplicação Flask, carregada via variáveis de ambiente, para assinar e proteger os cookies de sessão de usuário.
4. **Adicionar Proteção Contra CSRF:** Integrar tokens anti-CSRF nos formulários de login e cadastro (`Flask-WTF`) para coibir a submissão de requisições forjadas por terceiros.
5. **Adicionar Parâmetros de Integridade nas CDNs (SRI):** Incluir os atributos `integrity` e `crossorigin` nas chamadas externas do framework Bootstrap para blindar o frontend contra envenenamento de scripts.

---

## 🔍 Detalhamento das Vulnerabilidades Encontradas

### 1. Modo Depuração (Debug) Ativado em Ambiente Geral
* **Localização:** Arquivo `run.py`, linha de inicialização do servidor (`app.run(debug=True)`).
* **Descrição:** O framework Flask está configurado para rodar com o modo interativo de depuração ativado. Quando ocorre uma exceção ou erro na aplicação, um console interativo capaz de executar comandos arbitrários em Python é exposto diretamente na interface do navegador.
* **Evidência:**
  ```python
  if __name__ == '__main__':
      app.run(debug=True)




# Relatório de Inspeção e Mitigação de Segurança Web

**Disciplina:** Segurança de Sistemas Computacionais  
**Professor:** Fabio Vidal  
**Discente:** Marivaldo Lopes das Chagas  
**Data da Inspeção Inicial:** 14/05/2026  
**Data da Atualização / Mitigação:** 16/05/2026  
**Status Final:** 100% Corrigido (Conformidade com Diretrizes de Desenvolvimento Seguro)

---

## 1. Identificação Inicial de Vulnerabilidades (Relatório de Inspeção)

Durante a análise de segurança realizada no protótipo da aplicação Web de Help Desk (desenvolvida em Python com o framework Flask), foram identificados 5 achados críticos que necessitavam de correção imediata para mitigar riscos de invasão, vazamento de dados ou falsificação de requisições.

### Resumo dos Achados Originais:
1. **Modo Debug Ativo (`debug=True`):** Exposição de logs de erro detalhados e terminal interativo para usuários externos.
2. **Armazenamento de Senhas Vulnerável:** Tratamento e validação de credenciais em formato de texto limpo (plaintext).
3. **Ausência de Chave Secreta (`SECRET_KEY`):** Falta de uma assinatura criptográfica base para gerenciamento de sessões seguras.
4. **Vulnerabilidade a Ataques CSRF:** Formulários web expostos a falsificação de requisições por falta de tokens dinâmicos.
5. **Inclusão de Recursos Externos sem SRI:** Importação de estilos do Bootstrap sem validação de integridade por soma hash.

---

## 2. Detalhamento das Correções Executadas por Arquivo

Todas as vulnerabilidades listadas foram corrigidas diretamente na estrutura do projeto, testadas em ambiente local (Ubuntu/WSL) e sincronizadas com o repositório remoto via Git. Abaixo está o mapeamento das ações corretivas divididas pelos **4 arquivos estruturais do site**:

### 📄 2.1. Arquivo: `run.py` (Back-end Principal)
O arquivo de controle central da aplicação recebeu as principais diretrizes de segurança lógica e criptografia:
* **Mitigação do Achado 1 (Debug Mode):** Alteração do parâmetro de inicialização do servidor para `debug=False`, desativando a exibição de logs sensíveis em ambiente de produção.
* **Mitigação do Achado 2 (Hashing de Senhas):** Importação e implementação do módulo de segurança `Werkzeug`. O fluxo de cadastro foi atualizado para gerar hashes criptográficos irreversíveis via `generate_password_hash`, e a rota de login passou a validar as credenciais comparando hashes seguros através de `check_password_hash`.
* **Mitigação do Achado 3 (Secret Key):** Configuração da propriedade `app.config['SECRET_KEY']` utilizando uma string robusta para assinar criptograficamente as sessões dos usuários.
* **Mitigação do Achado 4 (Proteção CSRF):** Ativação global do componente `CSRFProtect` integrado ao ecossistema Flask.

### 📄 2.2. Arquivo: `templates/login.html` (Front-end)
A interface de autenticação do usuário recebeu camadas de proteção contra ataques direcionados e injeções de terceiros:
* **Mitigação do Achado 4 (Token Anti-CSRF):** Injeção de uma tag oculta de segurança (`input type="hidden"`) logo após a abertura da tag `<form>`. Essa tag carrega dinamicamente o valor do token gerado no back-end (`{{ csrf_token() }}`), inviabilizando requisições forjadas externas.
* **Mitigação do Achado 5 (Integridade de Subrecursos):** Substituição do link de importação simples do Bootstrap CSS por uma tag contendo as diretivas `integrity` (SHA-384) e `crossorigin`, impedindo o carregamento de estilos caso o servidor da CDN seja adulterado.

### 📄 2.3. Arquivo: `templates/cadastro.html` (Front-end)
A tela de criação de novas contas foi reestruturada seguindo os mesmos critérios rigorosos de conformidade aplicados ao login:
* **Mitigação do Achado 4 (Token Anti-CSRF):** Inclusão do campo invisível validador do token CSRF imediatamente abaixo da tag do formulário de cadastro (`<form action="/cadastro" method="post">`).
* **Mitigação do Achado 5 (Integridade de Subrecursos):** Atualização da folha de estilos externa do framework Bootstrap utilizando os atributos verificadores de soma hash para garantir a integridade do código importado.

### 📄 2.4. Arquivo: `templates/dashboard.html` (Front-end)
O painel de gerenciamento e exibição de relatórios internos da aplicação foi blindado contra contaminações de dependências:
* **Mitigação do Achado 5 (Integridade de Subrecursos):** Como este arquivo não possui formulários de envio (inputs do tipo POST), a correção focou na segurança da CDN. A chamada externa do framework Bootstrap foi atualizada com os parâmetros de validação `integrity` e `crossorigin`, garantindo que a área administrativa do Help Desk permaneça protegida contra injeções maliciosas em scripts externos.

---

## 3. Conclusão e Parecer Técnico Final

A auditoria e o plano de mitigação aplicados ao sistema de Help Desk da UAB foram concluídos com pleno êxito. Ao reestruturar os 4 arquivos essenciais do site (`run.py`, `login.html`, `cadastro.html` e `dashboard.html`), neutralizou-se com sucesso o conjunto de vulnerabilidades críticas mapeadas inicialmente (aderindo às boas práticas recomendadas pela OWASP). 

Todo o código protegido e o histórico detalhado de alterações encontram-se devidamente registrados e publicados na ramificação principal (`main`) do repositório remoto no GitHub para avaliação final da banca acadêmica.

