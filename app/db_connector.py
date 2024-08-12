# Bibliotecas de conexão
from sqlalchemy import create_engine
import psycopg2

# Classe de conexão com o BD
class DBConnector:
    # Método Construtor
    def __init__(self, database, user, password, host, port=5432):
        self.database = database  
        self.user = user
        self.password = password
        self.host = host
        self.conn = None
        self.engine = None
        self.port = port

    # Função estabelecer conexão
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                database = self.database,
                user = self.user,
                password = self.password,
                host = self.host,
                port = self.port
            )        
            self.engine = create_engine(f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')
            print("Conexão estabelecida com sucesso")
        except Exception as e:
            print(f"Erro ao conectar ao BD:{e}")
    
    # Função encerrar conexão
    def close(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            print("conexão fechada com sucesso")
    
    # Cursor para comandos SQL
    def get_cursor(self):
        if self.conn:
            return self.conn.cursor()
        else:
            print("primeiro estabeleça a conexão")
            return None
