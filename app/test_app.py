import pytest
from .db_connector import DBConnector
from .data_loader import DataLoader
from .data_cleaner import DataCleaner
from .data_validator import DataValidator
from unittest.mock import Mock

# Testes para a conexão ao banco de dados
def test_connect_to_db():
    db_config = {
        'database': 'db_clientes',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'db',
        'port': 5432
    }
    db = DBConnector(**db_config)
    db.connect()
    assert db.conn is not None
    db.close()

# Testes para a limpeza de dados
def test_higienizar_cpf():
    assert DataCleaner.higienizar_cpf("123.456.789-00") == "12345678900"

def test_higienizar_cnpj():
    assert DataCleaner.higienizar_cnpj("12.345.678/0001-00") == "12345678000100"

def test_substituir_null_por_vazio():
    import pandas as pd
    df = pd.DataFrame({"col1": ["NULL", "val1"]})
    df_clean = DataCleaner.substituir_null_por_vazio(df)
    assert df_clean.iloc[0, 0] == ""

# Testes para a validação de CPF/CNPJ
def test_validar_cpf():
    assert DataValidator.validar_cpf("12345678909") == False
    assert DataValidator.validar_cpf("12345678900") == True

def test_validar_cnpj():
    assert DataValidator.validar_cnpj("12345678000100") == False
    assert DataValidator.validar_cnpj("12345678000191") == True

# Testes para o carregamento de dados
def test_load_data(mocker):
    mock_cursor = Mock()
    data_loader = DataLoader("/app/dataset/base_teste.txt", "/app/dataset/base_teste_temp.csv", mock_cursor)
    
    # Mockando o pandas e o método de leitura de CSV
    mocker.patch("pandas.read_csv", return_value=mocker.Mock())
    
    data_loader.load_data()
    mock_cursor.copy_expert.assert_called_once()
