# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Carrega as variaveis do arquivo .env
load_dotenv()

# URL de conexão com o seu banco de dados MySQL
# Formato: "mysql+pymysql://USUARIO:SENHA@HOST/NOME_DO_BANCO"
# Le a variavel de ambiente
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Cria a engine de conexao com o banco
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria uma fabrica de conversas com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os modelos de tabela
Base = declarative_base()
