# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, text
from sqlalchemy.sql import func
from .database import Base

# Define a estrutura da tabela 'analises' no banco de dados
class Analise(Base):
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String(500), nullable=False)
    sentimento = Column(String(50), nullable=False)
    confianca = Column(Float, nullable=False)
    data_analise = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))