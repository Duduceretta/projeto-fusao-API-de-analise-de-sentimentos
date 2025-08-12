# API de Análise de Sentimentos com Scikit-Learn, FastAPI e MySQL

## Descrição

Este projeto implementa um sistema de Inteligência Artificial de ponta a ponta, desde o treinamento de um modelo de Machine Learning até sua implantação como uma API web interativa com persistência de dados.

- **Fase 1 (Análise e Treinamento):** Foi treinado um modelo de Machine Learning (`Regressão Logística` com `TF-IDF`) capaz de classificar reviews de produtos de um e-commerce brasileiro em três categorias: **positivo**, **negativo** ou **neutro**. O processo está documentado em um Jupyter Notebook.
- **Fase 2 (API Web):** O modelo treinado foi servido através de uma **API web utilizando FastAPI**, permitindo que previsões de sentimento sejam feitas em tempo real através de requisições HTTP.
- **Fase 3 (Persistência de Dados):** A API foi integrada a um banco de dados **MySQL utilizando SQLAlchemy**, garantindo que cada análise realizada seja salva para consultas e análises históricas.

## Tecnologias Utilizadas

- **Back-end & API:** Python 3.10+, FastAPI, Uvicorn
- **Machine Learning:** Scikit-learn, Pandas, Joblib
- **Banco de Dados:** MySQL, SQLAlchemy (ORM)
- **Outros:** Jupyter Notebook, Git, Variáveis de Ambiente (`.env`)

## Como Executar o Projeto

### Instalação

1.  **Clone este repositório:**
    ```bash
    git clone https://github.com/Duduceretta/projeto-fusao-API-de-analise-de-sentimentos.git
    ```
2.  **Navegue até a pasta do projeto:**
    ```bash
    cd projeto-fusao-API-de-analise-de-sentimentos
    ```
3.  **Crie e ative um ambiente virtual:**
    ```bash
    # Criar venv
    python -m venv venv
    # Ativar no Windows
    .\venv\Scripts\activate
    # Ativar no Mac/Linux
    source venv/bin/activate
    ```
4.  **Instale as dependências:**
    ```bash
    python -m pip install -r requirements.txt
    ```
5.  **Importante (Para a Fase 1):** Baixe o dataset de reviews do [Kaggle (Olist Brazilian E-Commerce)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) e coloque o arquivo `olist_order_reviews_dataset.csv` na pasta raiz do projeto.

### Configuração do Banco de Dados

1.  **Crie um banco de dados MySQL** com o nome `db_sentimentos`.
2.  **Configure as variáveis de ambiente:** Na raiz do projeto, renomeie o arquivo `.env.example` para `.env` e preencha com suas credenciais do MySQL.
    ```env
    DATABASE_URL="mysql+pymyssecret://SEU_USUARIO:SUA_SENHA@localhost/db_sentimentos"
    ```
3.  **Crie as tabelas no banco:** Execute o script utilitário para criar a tabela `analises`:
    ```bash
    python create_tables.py
    ```

### Parte 1: Análise e Treinamento do Modelo (Opcional)

O notebook `analise_sentimentos.ipynb` contém todo o passo a passo do processo de análise, treinamento e avaliação do modelo. Os artefatos finais (`modelo.joblib` e `vetorizador.joblib`) já estão incluídos neste repositório, então não é necessário executar o notebook para rodar a API.

Para explorar o notebook, rode o comando:

```bash
jupyter notebook analise_sentimentos.ipynb
```

### Parte 2: Executando a API de Análise de Sentimentos

Inicie o servidor da API: Com o ambiente virtual ativo, rode o seguinte comando no terminal:

```bash
python -m uvicorn app.main:app --reload
```

A API estará disponível em http://127.0.0.1:8000.

Teste de forma interativa: Acesse a documentação gerada automaticamente pelo FastAPI:
http://127.0.0.1:8000/docs

Agora você pode testar os dois endpoints:

- POST /analisar-sentimento: Envie um texto e veja a análise. Essa ação também salvará o resultado no banco de dados.

- GET /historico: Consulte o histórico das últimas 10 análises salvas no banco.

## Resultados

O modelo treinado (Regressão Logística com TF-IDF) alcançou os seguintes resultados no conjunto de teste da Fase 1:

<img width="804" height="323" alt="image" src="https://github.com/user-attachments/assets/85a9c807-96de-4873-9f6c-17e9000ddc10" />
