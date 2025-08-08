# Criacao da api.

# Import das ferramentas necessarias.
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

# Criando a instancia da aplicacao FastAPI.
app = FastAPI()

# Carrega os arquivos de IA (modelo e vetorizador) na memoria.
# Isso acontece UMA vez, quando a Api é iniciada (desempenho bom).
# Evita de carregar um novo modelo para cada nova requisicao (desempenho ruim).
try:
    modelo = joblib.load('modelo.jolib')
    vetorizador = joblib.load('vetorizador.jolib')
    print("Modelo e vetorizador carregados com sucesso!")
except FileNotFoundError:
    print("Erro: Arquivos 'modelo.jolib' ou 'vetorizador.jolib' nao encontrados.")
    modelo = None
    vetorizador = None

# Criando uma rota de "health check" para verificar se a API esta no ar.
@app.get("/")
def health_check():
    return {"status": "API esta no ar e o modelo parece estar carregado" if modelo else "API esta no ar, mas o modelo nao pode ser carregado."}

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
    confainca: float

@app.post("/analisar-sentimento", response_model=SentimentResponse)
def analisar_sentimento(request: SentimentRequest):
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

    # 5. Montar e retornar a resposta final seguindo o contrato.
    return SentimentResponse (
        sentimento=sentimento_predito,
        confainca=confianca_predicao
    )
