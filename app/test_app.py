# Script de Testes

import pandas as pd
import pytest
import time
from psycopg2 import connect
from pytest_postgresql import factories

# TESTE01: DATA_CLEANER.
from app.data_cleaner import DataCleaner

def test_higienizar_cpf():
    assert DataCleaner.higienizar_cpf('123.456.789-00') == '12345678900'
    assert DataCleaner.higienizar_cpf('000.000.000-00') == '00000000000'
    assert DataCleaner.higienizar_cpf('12345678900') == '12345678900'

def test_higienizar_cnpj():
    assert DataCleaner.higienizar_cnpj('12.345.678/0001-99') == '12345678000199'
    assert DataCleaner.higienizar_cnpj('00.000.000/0000-00') == '00000000000000'
    assert DataCleaner.higienizar_cnpj('12345678000199') == '12345678000199'

def test_garantir_tipo_numerico():
    df = pd.DataFrame({
        'col1': ['1234,34', '5678,58', '9000,45'],
        'col2': ['123,33', '456,88', '789,89']
    })
    df = DataCleaner.garantir_tipo_numerico(df, ['col1', 'col2'])
    assert df['col1'].iloc[0] == 1234.34
    assert df['col1'].iloc[1] == 5678.58
    assert df['col1'].iloc[2] == 9000.45
    assert df['col2'].iloc[0] == 123.33
    assert df['col2'].iloc[1] == 456.88
    assert df['col2'].iloc[2] == 789.89

def test_substituir_null_por_vazio():
    df = pd.DataFrame({
        'col1': ['a', 'NULL', 'b'],
        'col2': ['NULL', 'c', 'NULL']
    })
    df = DataCleaner.substituir_null_por_vazio(df)
    assert df['col1'].iloc[0] == 'a'
    assert df['col1'].iloc[1] == ''
    assert df['col1'].iloc[2] == 'b'
    assert df['col2'].iloc[0] == ''
    assert df['col2'].iloc[1] == 'c'
    assert df['col2'].iloc[2] == ''

# TESTE02: DATA_VALIDATOR
from app.data_validator import DataValidator

def test_validar_cpf():
    assert DataValidator.validar_cpf('04109164125') == True
    assert DataValidator.validar_cpf('05818942198') == True  
    assert DataValidator.validar_cpf('79379491000850') == False  # CPF inválido
    assert DataValidator.validar_cpf('79379491000851') == False  # CPF inválido

def test_validar_cnpj():
    assert DataValidator.validar_cnpj('79379491000850') == True   
    assert DataValidator.validar_cnpj('04109164125') == False  # CNPJ inválido

# TESTE03: DATA_LOADER
from app.data_loader import DataLoader

# Cria um banco de dados PostgreSQL em memória
postgres_mydb = factories.postgresql_noproc(
    host='localhost', port=5432, user='postgres', password='password'
)
time.sleep(30)
@pytest.fixture
def db_cursor(postgres_mydb):
    conn = connect(
        dbname=postgres_mydb.dbname,
        user=postgres_mydb.user,
        password=postgres_mydb.password,
        host=postgres_mydb.host,
        port=postgres_mydb.port
    )
    cursor = conn.cursor()

    # Cria a tabela base_teste no banco de dados
    cursor.execute("""
    CREATE TABLE base_teste (
        CPF VARCHAR(14),
        PRIVATE VARCHAR(255),
        INCOMPLETO VARCHAR(255),
        DATA_ULTIMA_COMPRA DATE,
        TICKET_MEDIO NUMERIC,
        TICKET_ULTIMA_COMPRA NUMERIC,
        LOJA_MAIS_FREQUENTE VARCHAR(255),
        LOJA_ULTIMA_COMPRA VARCHAR(255),
        CPF_VALIDO BOOLEAN,
        CNPJ_LMF_VALIDO BOOLEAN,
        CNPJ_LUC_VALIDO BOOLEAN
    )
    """)
    conn.commit()
    
    yield cursor
    
    cursor.close()
    conn.close()

def test_load_data(db_cursor):
    input_file = 'test_input.txt'
    temp_file = 'test_temp.csv'
    
    # Crie um arquivo de teste com dados fictícios
    test_data = """\
    123.456.789-00 NULL 1 2021-01-01 1,234 5,678 NULL NULL
    234.567.890-11 NULL 2 2021-02-01 2,345 6,789 NULL NULL
    """
    with open(input_file, 'w') as f:
        f.write(test_data)

    # Instanciar o DataLoader e chamar o método load_data
    loader = DataLoader(input_file, temp_file, db_cursor)
    loader.load_data()
    
    # Verifique se os dados foram carregados corretamente
    db_cursor.execute("SELECT COUNT(*) FROM base_teste")
    count = db_cursor.fetchone()[0]
    assert count == 2, "Número de registros na tabela base_teste está incorreto."

    # Verifique se o arquivo temporário foi criado
    df_temp = pd.read_csv(temp_file, header=None)
    assert not df_temp.empty, "O arquivo temporário está vazio."








