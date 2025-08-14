# test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Cria um cliente de teste que conversa com a api
client = TestClient(app) 

# --- Testes de Sanidade ---
def test_health_check_deve_retornar_200_e_mensagem_ok():
    """Testa se a API esta funcionando"""
    # 1. Acao (Arrange): Fazer uma requisicao get para a rota "/"
    response = client.get("/")

    # 2. Verificacao (Assert): O status de resposta foi 200 (OK)?
    assert response.status_code == 200

    # 3. Verificacao (Assert): O corpo da resposta JSON e o que esperamos?
    assert response.json() == {"status": "API esta no ar!"}

# --- Testes de Validacao de Entrada ---
def test_analisar_sentimento_com_chave_invalida_deve_retornar_422():
    """Testa se a API rejeita um JSON qunado a chave for invalida."""
    response = client.post(
        "/analisar-sentimento", 
        json={"frase": "Isso vai dar erro."}
    )
    assert response.status_code == 422


def test_analisar_sentimento_com_payload_vazio_deve_retornar_422():
    """Testa se a API rejeita um JSON vazio que nao contem a chave 'texto'."""
    response = client.post(
        "/analisar-sentimento", 
        json={}
    )
    assert response.status_code == 422


def test_analisar_sentimento_com_tipo_de_dado_errado_deve_retornar_422():
    """Testa se a API rejeita um payload onde o valor de 'texto' nao e uma string."""
    response = client.post(
        "/analisar-sentimento", 
        json={"texto": 1234}
    )
    assert response.status_code == 422

# --- Testes de logica de modelo ---
def test_analisar_sentimento_com_frase_positiva():
    """Testa se uma frase claramente positiva retorna um sentimento 'positivo'."""
    response = client.post(
        "/analisar-sentimento",
        json={"texto": "Que produto maravilhoso! Recomendo a todos, entrega super rápida."}    
    )

    data = response.json()
    assert response.status_code == 200
    assert data["sentimento"] == "positivo"
    assert 0 <= data["confianca"] <= 1


def test_analisar_sentimento_com_payload_invalido_retorna_detalhe_de_erro():
    """Testa se a API informa qual campo esta faltando em um payload invalido."""
    response = client.post(
        "/analisar-sentimento", 
        json={"frase": "Payload invalido"}
    )

    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["msg"] == "Field required"
    assert data["detail"][0]["loc"] == ["body", "texto"] 


def test_analisar_sentimento_com_frase_negativa():
    """Testa se uma frase claramente negativa retorna um sentimento 'negativo'."""
    response = client.post(
        "/analisar-sentimento",
        json={"texto": "Odeio esse produto. A qualidade é péssima e veio quebrado."}    
    )

    data = response.json()
    assert response.status_code == 200
    assert data["sentimento"] == "negativo"
    assert 0 <= data["confianca"] <= 1


# Marca como uma falha esperada (Ajuste futuro)
@pytest.mark.xfail(reason="O modelo atual tem dificuldade em classificar frases neutras")
def test_analisar_sentimento_com_frase_neutra():
    """Testa se uma frase neutra retorna um sentimento 'neutro'."""
    response = client.post(
        "/analisar-sentimento",
        json={"texto": "A entrega do produto foi realizada hoje."}    
    )

    data = response.json()
    assert response.status_code == 200
    assert data["sentimento"] == "neutro"
    assert 0 <= data["confianca"] <= 1