# app/schemas.py
from pydantic import BaseModel
from datetime import datetime

# Contratos - Pdronizacao
# Definir o "contrato" de dados que a API espera receber no corpo do request.
# Esperamos um JSON com uma chave "texto" do tipo string.
class SentimentRequest(BaseModel):
    texto: str

# Definir o "contrato" de dados que a API vai devolver como resposta.
# A resposta sera um JSON com "sentimento" e "confianca".
class SentimentResponse(BaseModel):
    sentimento: str
    # Define uma probabilidade para cada tipo positivo/negativo/neutro.
    # Pega a maior, ou seja, "esse texto tem maior probabilidade de ser do tipo positivo/negativo/neutro".
    confianca: float

# Define o contrato do JSON como resposta
class AnaliseResponse(BaseModel):
    id: int
    texto: str
    sentimento: str
    confianca: float
    data_analise: datetime

    class Config:
        from_attributes = True
