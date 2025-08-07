# Projeto de Análise de Sentimentos com Scikit-Learn

## Descrição

Este projeto faz parte da Fase 1 de um sistema completo de IA. O objetivo aqui foi treinar um modelo de Machine Learning capaz de classificar reviews de produtos de um e-commerce brasileiro em três categorias: positivo, negativo ou neutro.

## Tecnologias Utilizadas

- Python 3.x
- Pandas
- Scikit-learn
- Jupyter Notebook
- Joblib

## Como Executar o Projeto

1. Clone este repositório: `git clone [URL_DO_SEU_REPO]`
2. Navegue até a pasta do projeto: `cd projeto-fusao-ia`
3. Crie e ative um ambiente virtual: `python -m venv venv` e `source venv/bin/activate` (ou `.\venv\Scripts\activate` no Windows).
4. Instale as dependências: `pip install -r requirements.txt`
5. **Importante:** Baixe o dataset de reviews do [Kaggle (Olist Brazilian E-Commerce)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) e coloque o arquivo `olist_order_reviews_dataset.csv` na pasta raiz do projeto.
6. Abra o Jupyter Notebook: `jupyter notebook analise_sentimentos.ipynb`

## Resultados

O modelo treinado (Regressão Logística com TF-IDF) alcançou os seguintes resultados no conjunto de teste:

_(AQUI VOCÊ COLA UM PRINT DO SEU `classification_report`!)_
