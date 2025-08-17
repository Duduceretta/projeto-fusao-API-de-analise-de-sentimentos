# main.py

import os
from typing import List

import joblib
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db

# Descobre o caminho absoluto para o diretório onde este arquivo (main.py) está
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
# Constrói o caminho para a pasta raiz (um nível acima da pasta 'app')
PASTA_RAIZ = os.path.dirname(DIRETORIO_ATUAL)
# Constrói o caminho completo para os arquivos do modelo
CAMINHO_MODELO = os.path.join(PASTA_RAIZ, 'modelo.joblib')
CAMINHO_VETORIZADOR = os.path.join(PASTA_RAIZ, 'vetorizador.joblib')

# Criando a instancia da aplicacao FastAPI.
app = FastAPI(
    title="API de Análise de Sentimentos",
    version="1.0.0",
    description="Uma API que utiliza um modelo de Machine Learning para classificar o sentimento de textos em português.",
)

# Carrega os arquivos de IA (modelo e vetorizador) na memoria.
# Isso acontece UMA vez, quando a Api é iniciada (desempenho bom).
# Evita de carregar um novo modelo para cada nova requisicao (desempenho ruim).
try:
    modelo = joblib.load(CAMINHO_MODELO)
    vetorizador = joblib.load(CAMINHO_VETORIZADOR)
    print("Modelo e vetorizador carregados com sucesso!")
except FileNotFoundError:
    print(f"Erro: Arquivos de modelo nao encontrados nos caminhos {CAMINHO_MODELO} e {CAMINHO_VETORIZADOR}")
    modelo = None
    vetorizador = None

# Criando uma rota de "health check" para verificar se a API esta no ar.
@app.get("/")
def health_check():
    return {"status": "API esta no ar!"}

# Criando uma rota que retorna as ultimas 10 analises feitas
@app.get("/historico", response_model=List[schemas.AnaliseResponse])
def get_historico_analises(db: Session = Depends(get_db)):
    ultimas_analises = db.query(models.Analise).order_by(models.Analise.data_analise.desc()).limit(10).all()
    return ultimas_analises

@app.post("/analisar-sentimento", response_model=schemas.SentimentResponse)
def analisar_sentimento(request: schemas.SentimentRequest, db: Session = Depends(get_db)): # Adicionada dependencia do banco
    # Garantir que o modelo foi carregado antes de tentar usar.
    if not modelo or not vetorizador:
        return {"sentimento": "erro", "confianca": 0.0}
    
    # 1. Pegar o texto que o usuario digitou.
    texto_usuario = [request.texto]

    # 2. Usar o vetorizador para transformar o texto em numeros.
    texto_vetorizado = vetorizador.transform(texto_usuario)

    # 3. Usar o modelo para fazer a predicao.
    previsao = modelo.predict(texto_vetorizado)
    probabilidade = modelo.predict_proba(texto_vetorizado)

    # 4. Formatar a resposta
    sentimento_predito = previsao[0]
    confianca_predicao = max(probabilidade[0]) 

    # Salvar previsao no banco de dados
    # 1. Cria um objeto do modelo do banco de dados
    nova_analise = models.Analise(
        texto=request.texto,
        sentimento=sentimento_predito,
        confianca=confianca_predicao
    )

    # Adiciona o objeto a uma sessao (prepara para salvar)
    db.add(nova_analise)
    
    # Confirma a transacao (salva no banco)
    db.commit()
    
    # Atualiza o objeto com os dados que o banco gerou (como ID e a data)
    db.refresh(nova_analise)

    # 5. Montar e retornar a resposta final seguindo o contrato.
    return schemas.SentimentResponse (
        sentimento=sentimento_predito,
        confianca=confianca_predicao
    )
