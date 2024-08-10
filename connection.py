import psycopg2
import csv
import time
import pandas as pd
from sqlalchemy import create_engine

time.sleep(40)

conn = psycopg2.connect(
    database="db_clientes",
    user="postgres",
    password="postgres",
    host="db"
)

cur = conn.cursor()
cur.execute("TRUNCATE TABLE base_teste;")

# Lendo o arquivo txt
df = pd.read_csv('/app/dataset/base_teste.txt', header=None, sep='\s+', skiprows=1, )

# Criando uma conexão com o banco de dados PostgreSQL
engine = create_engine('postgresql+psycopg2://postgres:postgres@db:5432/db_clientes')

# Converter vírgulas em pontos nas colunas numéricas
df[4] = df[4].astype(str).str.replace(',', '.')
df[5] = df[5].astype(str).str.replace(',', '.')

# Garantir que as colunas são do tipo numérico
df[4] = pd.to_numeric(df[4], errors='coerce')
df[5] = pd.to_numeric(df[5], errors='coerce')

# Ajustar os nomes das colunas
df.columns = ["CPF", "PRIVATE", "INCOMPLETO", "DATA_ULTIMA_COMPRA", "TICKET_MEDIO", "TICKET_ULTIMA_COMPRA", "LOJA_MAIS_FREQUENTE", "LOJA_ULTIMA_COMPRA"]

# Inserindo o DataFrame no banco de dados
#df.to_sql('base_teste', engine, if_exists='append', index=False, chunksize=1000)

df.to_csv('/app/dataset/base_teste_temp.csv', index=False, header=False)

# Usando COPY para carregar os dados
with open('/app/dataset/base_teste_temp.csv', 'r') as f:
    cur.copy_expert("COPY base_teste FROM STDIN WITH CSV", f)

# Abrir o arquivo TXT e ler os dados
#with open('/app/dataset/base_teste.txt', 'r') as file:
#    reader = csv.reader(file, delimiter=' ')  # Delimitador de tabulação
#    next(reader)  # Pular a linha do cabeçalho

#    for row in reader:
#        # Verificar o comprimento da linha
#        if len(row) != 8:
#            print(f"Linha com número incorreto de colunas (esperado 8, encontrado {len(row)}): {row}")
#            continue

        # Substituir valores vazios por None para tratamento de nulos
#        processed_row = [None if field == '' else field for field in row]
#
#        try:
#            # Executar a inserção com os dados processados
#            cur.execute("""
#                INSERT INTO base_teste ("CPF", "PRIVATE", "INCOMPLETO", "DATA DA ÚLTIMA COMPRA", 
#                "TICKET MÉDIO", "TICKET DA ÚLTIMA COMPRA", "LOJA MAIS FREQUÊNTE", "LOJA DA ÚLTIMA COMPRA") 
#                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#            """, processed_row)
#        except Exception as e:
#            print(f"Erro ao inserir a linha: {processed_row}")
#            print(e)

# Confirmar as mudanças no banco de dados
conn.commit()
cur.close()
conn.close()