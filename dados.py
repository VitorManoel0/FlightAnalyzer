from io import StringIO

import pandas as pd
from sqlalchemy import create_engine
from conexao import init_app
import requests


def create_mercado(row):
    mercado = ''.join(sorted({row['AEROPORTO_DE_ORIGEM_SIGLA'], row['AEROPORTO_DE_DESTINO_SIGLA']}))
    return mercado


def return_data(url):
    print('Iniciando a stream de dados')

    response = requests.get(url)

    if response.status_code == 200:

        df = pd.read_csv(StringIO(response.text), skiprows=1, sep=';')

        return df

    else:
        print("Falha ao acessar a URL")


def filter_data():
    DATABASE_URL = init_app()

    engine = create_engine(DATABASE_URL)

    df = return_data('https://sistemas.anac.gov.br/dadosabertos/Voos%20e%20opera%C3%A7%C3%B5es%20a%C3'
                     '%A9reas/Dados%20Estat%C3%ADsticos%20do%20Transporte%20A%C3%A9reo/Dados_Estatisticos'
                     '.csv')

    df2 = return_data('https://sistemas.anac.gov.br/dadosabertos/Voos%20e%20opera%C3%A7%C3%B5es%20a%C3'
                      '%A9reas/Dados%20Estat%C3%ADsticos%20do%20Transporte%20A%C3%A9reo'
                      '/Dados_Estatisticos_parte.csv')

    filter_columns = ['EMPRESA_SIGLA', 'GRUPO_DE_VOO', 'NATUREZA', 'AEROPORTO_DE_ORIGEM_SIGLA',
                      'AEROPORTO_DE_DESTINO_SIGLA', 'RPK', 'ANO', 'MES']

    df_filter = df[filter_columns].dropna()
    df_filter2 = df2[filter_columns].dropna()

    df_merged = pd.merge(df_filter, df_filter2, how='outer')

    df_merged = df_merged.loc[(df_merged['EMPRESA_SIGLA'] == 'GLO') & (df_merged['GRUPO_DE_VOO'] == 'REGULAR') &
                              (df_merged['NATUREZA'] == 'DOMÉSTICA')]

    df_merged['MERCADO'] = df_merged.apply(lambda row: create_mercado(row), axis=1)

    filter_columns = ['ANO', 'MES', 'MERCADO', 'RPK']

    df_merged = df_merged[filter_columns]
    df_merged.columns = df_merged[filter_columns].columns.str.lower()

    df_merged.to_sql('flights', con=engine, if_exists='append', index=False)

    return df_merged
