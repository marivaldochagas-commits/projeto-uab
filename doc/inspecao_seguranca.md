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

