from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

# Configuração do banco de dados MySQL
# Senha com caracteres especiais precisa de URL encoding
DB_USER = "dbamysql"
DB_PASSWORD = quote_plus("@Fn.2026@")  # Codifica @ como %40
DB_HOST = "76.13.69.127"
DB_PORT = "3306"
DB_NAME = "dbApiTarefasFamilia"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
