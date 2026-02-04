from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base
from app.routers import local, tarefa, usuario, tarefa_usuario, category

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Root path para servidor (vazio para local)
ROOT_PATH = os.getenv("ROOT_PATH", "")

# Criação da aplicação FastAPI com configuração do Swagger
app = FastAPI(
    title="API Tarefas Família",
    description="""
## API para gerenciamento de tarefas familiares

Esta API permite gerenciar:
* **Locais** - Locais onde as tarefas são realizadas
* **Tarefas** - Tarefas a serem realizadas
* **Usuários** - Membros da família
* **Atribuições** - Relação entre tarefas e usuários
* **Categorias** - Categorias de tarefas

### Funcionalidades principais:
- CRUD completo para todas as entidades
- Atribuição de tarefas a membros da família
- Marcação de tarefas como concluídas
- Filtros por usuário e local
    """,
    version="1.0.0",
    root_path=ROOT_PATH,
    docs_url="/swagger",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão dos routers
app.include_router(local.router)
app.include_router(tarefa.router)
app.include_router(usuario.router)
app.include_router(tarefa_usuario.router)
app.include_router(category.router)


@app.get("/", tags=["Root"])
def root():
    """Endpoint raiz da API"""
    return {
        "message": "Bem-vindo à API Tarefas Família",
        "version": "1.0.0",
        "docs": "/swagger",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Verifica se a API está funcionando"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
