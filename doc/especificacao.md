# ESPECIFICAÇÃO TÉCNICA: SISTEMA DE ATENDIMENTO (TICKETS)

## 1. Configurações e Ambiente

### /requirements.txt
- **ação**: criar
- **descrição**: Gerenciamento de dependências para garantir que o ambiente de execução possua todas as bibliotecas necessárias.
- **pseudocódigo**:
  Flask==3.0.0
  Flask-SQLAlchemy==3.1.1
  Authlib==1.2.1
  python-dotenv==1.0.0
  gunicorn==21.2.0

### /.env.example
- **ação**: criar
- **descrição**: Arquivo de template para variáveis de ambiente sensíveis (segurança e credenciais).
- **pseudocódigo**:
  SECRET_KEY=string_aleatoria_segura
  DATABASE_PATH=app/db/atendimento.db
  PROPRIETARIO_EMAIL=proprietario@empresa.com
  PROPRIETARIO_PASSWORD=senha_segura_inicial
  DEBUG_MODE=True
  GOOGLE_CLIENT_ID=id_oauth_google
  GOOGLE_CLIENT_SECRET=secret_oauth_google

### /config.py
- **ação**: criar
- **descrição**: Módulo de configuração que carrega as variáveis de ambiente e define as configurações globais da aplicação Flask.
- **pseudocódigo**: 
  IMPORTAR os 
  IMPORTAR dotenv 
  EXECUTAR dotenv.load_dotenv() 
  CLASSE Config:
      DEFINIR SECRET_KEY COMO os.getenv("SECRET_KEY")
      DEFINIR SQLALCHEMY_DATABASE_URI COMO "sqlite:///" CONCATENADO COM os.getenv("DATABASE_PATH")
      DEFINIR DEBUG COMO BOOLEANO(os.getenv("DEBUG_MODE"))
      DEFINIR PROPRIETARIO_EMAIL COMO os.getenv("PROPRIETARIO_EMAIL")
      DEFINIR PROPRIETARIO_PASSWORD COMO os.getenv("PROPRIETARIO_PASSWORD")

---

## 2. Infraestrutura e Inicialização (Motor do Sistema)

### /Dockerfile
- **ação**: criar
- **descrição**: Definição da imagem do container para padronização do ambiente de desenvolvimento e produção.
- **pseudocódigo**:
  DEFINIR_IMAGEM_BASE python:3.10-slim
  DEFINIR_DIRETORIO_TRABALHO /app
  COPIAR requirements.txt PARA .
  EXECUTAR pip install -r requirements.txt
  COPIAR todo_conteudo PARA .
  EXPOR_PORTA 5000
  DEFINIR_COMANDO_INICIAL ["python", "run.py"]

### /app/database.py
- **ação**: criar
- **descrição**: Singleton da instância do SQLAlchemy para acesso global ao banco de dados.
- **pseudocódigo**:
  IMPORTAR SQLAlchemy
  INSTANCIAR db = SQLAlchemy()

### /app/__init__.py
- **ação**: criar
- **descrição**: Application Factory responsável por acoplar as extensões e registrar os controladores (Blueprints).
- **pseudocódigo**:
  IMPORTAR Flask, Config, db
  FUNCAO create_app():
      INSTANCIAR app = Flask(__name__)
      CARREGAR_CONFIGURACOES(app, Config)
      INICIALIZAR_EXTENSAO(db, app)
      REGISTRAR_BLUEPRINTS(auth, usuario, ticket, relatorio)
      RETORNAR app

### /run.py
- **ação**: criar
- **descrição**: Script de entrada. Responsável pelo "Bootstrap" do banco e do usuário mestre.
- **pseudocódigo**:
  IMPORTAR create_app, db, UsuarioModel, Config
  INSTANCIAR app = create_app()
  SE_ARQUIVO_EXECUTADO_DIRETAMENTE:
      COM CONTEXTO_DA_APLICACAO(app):
          CRIAR_TABELAS_BANCO_DE_DADOS(db)
          SE proprietario NAO EXISTE:
              CRIAR novo_proprietario(email=Config.PROPRIETARIO_EMAIL, role="PROPRIETARIO")
              novo_proprietario.set_senha(Config.PROPRIETARIO_PASSWORD)
              SALVAR_NO_BANCO()
      INICIAR_SERVIDOR(app, host="0.0.0.0", port=5000)

---

## 3. Camada de Dados (Persistência)

### /app/models/usuario_model.py
- **descrição**: Modelo de Usuário. Implementa controle de acesso (RBAC) e rastreabilidade de hierarquia.
- **pseudocódigo**:
  CLASSE UsuarioModel:
      COLUNA id: INTEIRO, CHAVE_PRIMARIA
      COLUNA email: TEXTO, UNICO
      COLUNA senha_hash: TEXTO
      COLUNA role: ENUM("PROPRIETARIO", "ADMINISTRADOR", "ATENDENTE", "CLIENTE")
      COLUNA criado_por_id: INTEIRO, FK("usuarios.id")

### /app/models/ticket_model.py
- **descrição**: Modelo de Ticket. Armazena o ciclo de vida dos chamados.
- **pseudocódigo**:
  CLASSE TicketModel:
      COLUNA id: INTEIRO, CHAVE_PRIMARIA
      COLUNA cliente_id: FK("usuarios.id")
      COLUNA atendente_id: FK("usuarios.id"), NULO
      COLUNA assunto: TEXTO
      COLUNA status: ENUM("ABERTO", "EM_ANDAMENTO", "RESOLVIDO")
      COLUNA data_criacao: TIMESTAMP

---

## 4. Lógica de Negócio (Controladores e Endpoints)

### /app/controllers/relatorio_controller.py
- **ação**: criar
- **descrição**: Motor de agregação de dados para visualização gerencial.
- **pseudocódigo**:
  ROTA "/admin/relatorios" [GET]:
      APLICAR requer_roles(["ADMINISTRADOR", "PROPRIETARIO"])
      
      # Consultas de Agregação (SQL Alchemy Queries)
      ATRIBUIR total_geral = db.session.query(TicketModel).count()
      ATRIBUIR resolvidos = db.session.query(TicketModel).filter_by(status="RESOLVIDO").count()
      
      # Lógica de Hierarquia (Somente tickets da equipe do Admin logado)
      SE usuario_logado.role == "ADMINISTRADOR":
          ATRIBUIR tickets_equipe = db.session.query(TicketModel).join(UsuarioModel, TicketModel.atendente_id == UsuarioModel.id).filter(UsuarioModel.criado_por_id == usuario_logado.id).count()
      
      RETORNAR RENDERIZAR_TEMPLATE("admin/relatorios.html", total=total_geral, resolvidos=resolvidos, equipe=tickets_equipe)

### /app/controllers/usuario_controller.py
- **descrição**: Gestão de usuários. Garante que Admins criem apenas Atendentes vinculados.
- **pseudocódigo**:
  ROTA "/admin/atendentes" [POST]:
      APLICAR requer_roles(["ADMINISTRADOR"])
      INSTANCIAR novo = UsuarioModel(role="ATENDENTE", criado_por_id=session["user_id"])
      SALVAR_NO_BANCO(novo)

---

## 5. Segurança e Proteção de Rotas

### /app/utils/auth_utils.py
- **descrição**: Decoradores de autorização baseados em papéis de usuário.
- **pseudocódigo**:
  FUNCAO requer_roles(lista_permitida):
      SE session["usuario_role"] NAO ESTA EM lista_permitida:
          RETORNAR ERRO(403, "Acesso Negado")