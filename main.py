# Recursos:
from app.db_connector import DBConnector
from app.data_loader import DataLoader
import time
import pandas as pd
from validate_docbr import CPF, CNPJ

# Espera até que o banco esteja disponível.
time.sleep(30)

# Configuração e conexão com o BD.
db_config = {
    'database': 'db_clientes',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db'
}
db = DBConnector(**db_config)
db.connect()

# Execução de comando para truncar tabela.
cur = db.get_cursor()
cur.execute("TRUNCATE TABLE base_teste;")

# Configurações do carregamento de dados
input_file = '/app/dataset/base_teste.txt'
temp_file = '/app/dataset/base_teste_temp.csv'

# Criando uma instância de Carregamento e Carregando os Dados.
data_loader = DataLoader(input_file, temp_file, cur)
data_loader.load_data()

# Confirmar as mudanças no banco de dados
cur.close()
db.close()