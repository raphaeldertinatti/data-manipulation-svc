# Script de Testes

import pandas as pd
import pytest
import time
from psycopg2 import connect

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


