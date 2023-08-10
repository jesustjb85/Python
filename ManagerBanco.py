from psycopg2 import connect
from datetime import datetime
import pandas as pd

## conecta banco ##

def conecta_bd():
    conexao = connect(
        host="18.230.44.138",  # Endereço do banco de dados
        database="data_ims",  # Nome do banco de dados
        user="a5solutions",  # Nome de usuário
        password="@5s0lut10ns"  # Senha do usuário
    )
    return conexao

def renomear_colunas(df):
    novo_nome_colunas = {
        'dddtelefone1': 'fone_01',
        'dddtelefone2': 'fone_02',
        'dddtelefone3': 'fone_03',
        'dddtelefone4': 'fone_04',
        'nomecliente': 'nomecliente',
        'cep': 'cep',
        'sguf': 'estado',
        'codmailing': 'cod_mailing',
        'codchave': 'cod_chave'
    }
    try:
        df.rename(columns=novo_nome_colunas, inplace=True)
        return df
    except Exception as e:
        print("Erro ao renomear as colunas", e)
        return df

def ler_tabela(query_tabela):   
    try:
        conexao = conecta_bd()
        conexao.set_client_encoding('UTF8')
        df = pd.read_sql_query(query_tabela, conexao)
        return df   
    except Exception as e:
        print("Erro ao ler tabela", e)
        return None       
    finally:
        conexao.close()

def insere_na_tabela(lista_registros):
    try:
        conexao = connect(
        host="18.230.44.138",
        database="data_ims",
        user="a5solutions",
        password="@5s0lut10ns"
        )
        
        cursor = conexao.cursor()
        
        for registro in lista_registros:
            # Preparar a consulta SQL de inserção
            sql = """
                INSERT INTO leadteste (cdlead, fone_1, fone_2, fone_3, fone_4, nomecliente, cep, estado, cod_mailing, cod_chave)
                VALUES (%(cdlead)s, %(fone_01)s, %(fone_02)s, %(fone_03)s, %(fone_04)s, %(nomecliente)s, %(cep)s, %(estado)s, %(cod_mailing)s, %(cod_chave)s)
            """
            
            # Executar a consulta com os valores do registro atual
            cursor.execute(sql, registro)
        
        # Commit das alterações
        conexao.commit()
        
    except Exception as e:
        print("Erro ao inserir na tabela", e)
    finally:
        cursor.close()
        conexao.close()

def main():
    query_tabela = "SELECT dddtelefone1, dddtelefone2, dddtelefone3, dddtelefone4, nomecliente, cep, sguf, codmailing, codchave, cpfcnpj FROM a5solutions.lead_entrada limit 5"
    df_tabela = ler_tabela(query_tabela)

    if df_tabela is not None:
        df_tabela = renomear_colunas(df_tabela)
        
        # Transformar o DataFrame em uma lista de dicionários com as colunas específicas
        lista_registros = df_tabela[[
            'fone_01', 'fone_02', 'fone_03', 'fone_04', 'nomecliente', 'cep', 'estado', 'cod_mailing', 'cod_chave', 'cpfcnpj'
        ]].to_dict('records')
        
        # Preencher as demais colunas do dicionário com valores nulos
        for registro in lista_registros:
            for coluna in ['fone_01', 'fone_02', 'fone_03', 'fone_04', 'nomecliente', 'cep', 'estado', 'cod_mailing', 'cod_chave']:
                if coluna not in registro:
                    registro[coluna] = None
        
        # Preencher a coluna 'cdlead' com combinação de 'cpfcnpj' e sufixo
        for registro in lista_registros:
            cpfcnpj = registro['cpfcnpj']
            data = datetime.now()
            ano = data.year
            mes = data.month
            dia = data.day
            if dia < 15:
                semana = 'Q01'
            else:
                semana = 'Q02'
            sufixo =  f"{ano}{mes:02d}{semana}"
            registro['cdlead'] = f"{cpfcnpj}_{sufixo}"

        # Chamar a função para inserir os registros na tabela
        insere_na_tabela(lista_registros)

    else:
        print("O DataFrame está vazio.")

if __name__ == '__main__':
    main()

