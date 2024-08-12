# tests/test_datacleaner.py

import pandas as pd
import pytest
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
        'col1': ['1,234', '5.678', '9,000'],
        'col2': ['1,23', '4.56', '7,89']
    })
    df = DataCleaner.garantir_tipo_numerico(df, ['col1', 'col2'])
    assert df['col1'].iloc[0] == 1234.0
    assert df['col1'].iloc[1] == 5678.0
    assert df['col1'].iloc[2] == 9000.0
    assert df['col2'].iloc[0] == 1.23
    assert df['col2'].iloc[1] == 4.56
    assert df['col2'].iloc[2] == 7.89

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
