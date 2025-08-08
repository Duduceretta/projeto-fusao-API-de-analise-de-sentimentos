# API de Análise de Sentimentos com Scikit-Learn e FastAPI

## Descrição

Este projeto implementa um sistema de Inteligência Artificial de ponta a ponta, desde o treinamento de um modelo de Machine Learning até sua implantação como uma API web interativa.

- **Fase 1 (Análise e Treinamento):** Foi treinado um modelo de Machine Learning (`Regressão Logística` com `TF-IDF`) capaz de classificar reviews de produtos de um e-commerce brasileiro em três categorias: **positivo**, **negativo** ou **neutro**. Todo o processo de exploração e treinamento está documentado em um Jupyter Notebook.
- **Fase 2 (API e Produção):** O modelo treinado foi servido através de uma **API web utilizando FastAPI**, permitindo que previsões de sentimento sejam feitas em tempo real através de requisições HTTP.

## Tecnologias Utilizadas

- Python 3.10+
- Pandas (para manipulação de dados)
- Scikit-learn (para o modelo de ML)
- Joblib (para salvar e carregar o modelo)
- Jupyter Notebook (para análise exploratória)
- **FastAPI** (para a construção da API)
- **Uvicorn** (para rodar o servidor da API)

## Como Executar o Projeto

### Instalação

1.  **Clone este repositório:**
    ```bash
    git clone [https://github.com/Duduceretta/projeto-fusao-API-de-analise-de-sentimentos.git](https://github.com/Duduceretta/projeto-fusao-API-de-analise-de-sentimentos.git)
    ```
2.  **Navegue até a pasta do projeto:**
    ```bash
    cd projeto-fusao-ia
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
    pip install -r requirements.txt
    ```
5.  **Importante (Para a Fase 1):** Baixe o dataset de reviews do [Kaggle (Olist Brazilian E-Commerce)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) e coloque o arquivo `olist_order_reviews_dataset.csv` na pasta raiz do projeto.

### Parte 1: Análise e Treinamento do Modelo (Opcional)

O notebook `analise_sentimentos.ipynb` contém todo o passo a passo do processo de análise, treinamento e avaliação do modelo. Os artefatos finais (`modelo.joblib` e `vetorizador.joblib`) já estão incluídos neste repositório, então não é necessário executar o notebook para rodar a API.

Para explorar o notebook, rode o comando:

```bash
jupyter notebook analise_sentimentos.ipynb
```

### Parte 2: Executando a API de Análise de Sentimentos

Inicie o servidor da API: Com o ambiente virtual ativo, rode o seguinte comando no terminal:

```bash
uvicorn api:app --reload
```

A API estará disponível em http://127.0.0.1:8000.

Teste de forma interativa: Para uma experiência completa, acesse a documentação gerada automaticamente pelo FastAPI em seu navegador:
http://127.0.0.1:8000/docs

Nesta página, você pode expandir o endpoint POST /analisar-sentimento, clicar em "Try it out" e enviar seus próprios textos para ver a resposta do modelo em tempo real.

## Resultados

O modelo treinado (Regressão Logística com TF-IDF) alcançou os seguintes resultados no conjunto de teste da Fase 1:

<img width="804" height="323" alt="image" src="https://github.com/user-attachments/assets/85a9c807-96de-4873-9f6c-17e9000ddc10" />
