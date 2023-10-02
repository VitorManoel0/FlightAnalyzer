import app
import pandas as pd
from sqlalchemy import create_engine
from conexao import init_app

DATABASE_URL = init_app()

engine = create_engine(DATABASE_URL)


def create_mercado(row):
    mercado = ''.join(sorted({row['AEROPORTO_DE_ORIGEM_SIGLA'], row['AEROPORTO_DE_DESTINO_SIGLA']}))
    return mercado


def filter_data():
    df = pd.read_csv('dados/Dados_Estatisticos.csv', skiprows=1, sep=';')
    df2 = pd.read_csv('dados/Dados_Estatisticos_parte.csv', skiprows=1, sep=';')

    filter_columns = ['EMPRESA_SIGLA', 'GRUPO_DE_VOO', 'NATUREZA', 'AEROPORTO_DE_ORIGEM_SIGLA',
                      'AEROPORTO_DE_DESTINO_SIGLA', 'RPK']

    df_filter = df[filter_columns].dropna()
    df_filter2 = df2[filter_columns].dropna()

    df_merged = pd.merge(df_filter, df_filter2, how='outer')

    df_merged = df_merged.loc[(df_merged['EMPRESA_SIGLA'] == 'GLO') & (df_merged['GRUPO_DE_VOO'] == 'REGULAR') &
                              (df_merged['NATUREZA'] == 'DOMÉSTICA')]

    df_merged['MERCADO'] = df_merged.apply(lambda row: create_mercado(row), axis=1)

    df_merged.to_sql('Flights', con=engine, if_exists='replace', index=False)

    return df_merged


filter_data()
