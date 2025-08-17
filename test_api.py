# test_api.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import Analise

# Cria um banco de dados SQLite em memoria para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Cria a engine de testes
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)

# Cria uma fabrica de sessoes de teste
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para sobrecrever get_db do main app
def override_get_db():
    """
        Essa função sera usada no lugar da funcao get_db original durante os testes, garantindo que o banco de testes sera usado.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dizemos ao FastApi para utilizar override_get_db sempre get_db for chamado
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture()
def setup_and_teardown_db():
    """Fixture para criar as tabelas antes do teste e depois limpa-las."""
    # Setup: Cria as tabelas
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown: Limpa as tabelas
    Base.metadata.drop_all(bind=engine)

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
    
# --- Testes de logica de modelo ---
def test_analisar_sentimento_com_frase_positiva(setup_and_teardown_db):
    """Testa se uma frase claramente positiva retorna um sentimento 'positivo'."""
    response = client.post(
        "/analisar-sentimento",
        json={"texto": "Que produto maravilhoso! Recomendo a todos, entrega super rápida."}    
    )

    data = response.json()
    assert response.status_code == 200
    assert data["sentimento"] == "positivo"
    assert 0 <= data["confianca"] <= 1


def test_analisar_sentimento_com_frase_negativa(setup_and_teardown_db):
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
def test_analisar_sentimento_com_frase_neutra(setup_and_teardown_db):
    """Testa se uma frase neutra retorna um sentimento 'neutro'."""
    response = client.post(
        "/analisar-sentimento",
        json={"texto": "A entrega do produto foi realizada hoje."}    
    )

    data = response.json()
    assert response.status_code == 200
    assert data["sentimento"] == "neutro"
    assert 0 <= data["confianca"] <= 1

# --- Testes Banco de dados ---
def test_salva_analise_e_aparece_no_historico(setup_and_teardown_db):
    """Testa se cria uma analise e se retorna a analise vinda do historico."""
    texto_enviado = "Este e um teste de integracao!"
    
    response_post = client.post(
        "/analisar-sentimento",
        json={"texto": texto_enviado}    
    )
    assert response_post.status_code == 200

    response_get = client.get(
        "/historico"
    )
    assert response_get.status_code == 200

    historico = response_get.json()

    # O historico precisa ser uma lista
    assert isinstance(historico, list)

    # A lista nao esta vazia
    assert len(historico) > 0

    # Tem que ter somente uma analise no banco
    assert len(historico) == 1

    # O texto tem que ser o mesmo que enviamos
    assert historico[0]["texto"] == texto_enviado
