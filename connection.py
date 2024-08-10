import psycopg2
import time
import pandas as pd
from sqlalchemy import create_engine
from validate_docbr import CPF, CNPJ


time.sleep(40)

conn = psycopg2.connect(
    database="db_clientes",
    user="postgres",
    password="postgres",
    host="db"
)
cur = conn.cursor()
cur.execute("TRUNCATE TABLE base_teste;")

def validar_cpf(cpf):
    cpf_obj = CPF()
    return cpf_obj.validate(cpf)
def validar_cnpj(cnpj):
    cnpj_obj = CNPJ()
    return cnpj_obj.validate(cnpj)

# Lendo o arquivo txt
df = pd.read_csv('/app/dataset/base_teste.txt', header=None, sep='\s+', skiprows=1, )

# Validar CPFs e CNPJs
df['CPF_VALIDO'] = df[0].apply(lambda x: validar_cpf(str(x)))
df['CNPJ_LMF_VALIDO'] = df[6].apply(lambda x: validar_cnpj(str(x)) if pd.notna(x) else None)
df['CNPJ_LUC_VALIDO'] = df[7].apply(lambda x: validar_cnpj(str(x)) if pd.notna(x) else None)

# Criando uma conexão com o banco de dados PostgreSQL
engine = create_engine('postgresql+psycopg2://postgres:postgres@db:5432/db_clientes')

# Converter vírgulas em pontos nas colunas numéricas
df[4] = df[4].astype(str).str.replace(',', '.')
df[5] = df[5].astype(str).str.replace(',', '.')

# Garantir que as colunas são do tipo numérico
df[4] = pd.to_numeric(df[4], errors='coerce')
df[5] = pd.to_numeric(df[5], errors='coerce')

# Ajustar os nomes das colunas
df.columns = ["CPF", "PRIVATE", "INCOMPLETO", "DATA_ULTIMA_COMPRA", "TICKET_MEDIO", "TICKET_ULTIMA_COMPRA", "LOJA_MAIS_FREQUENTE", "LOJA_ULTIMA_COMPRA", "CPF_VALIDO", "CNPJ_LMF_VALIDO", "CNPJ_LUC_VALIDO"]

df.to_csv('/app/dataset/base_teste_temp.csv', index=False, header=False)

# Usando COPY para carregar os dados
with open('/app/dataset/base_teste_temp.csv', 'r') as f:
    cur.copy_expert("COPY base_teste FROM STDIN WITH CSV", f)

# Confirmar as mudanças no banco de dados
conn.commit()
cur.close()
conn.close()