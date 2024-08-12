# Importação da Biblioteca Pandas:
import pandas as pd
from app.data_cleaner import DataCleaner
from app.data_validator import DataValidator

# Classe de carga de dados
class DataLoader:
    # Método Construtor
    def __init__(self, input_file, temp_file, cursor):
       self.input_file = input_file
       self.temp_file = temp_file
       self.cursor = cursor  

    # Lê os dados do arquivo txt e carrega no banco de dados."   
    def load_data(self):
        try:
            # Lendo o arquivo.
            df = pd.read_csv(self.input_file, header=None, sep='\s+', skiprows=1)
            print(f"Arquivo {self.input_file} lido com sucesso.") 

            # Substituindo 'NULL' por ''
            df = DataCleaner.substituir_null_por_vazio(df)

            # Aplicando limpeza de dados
            df[0] = df[0].apply(DataCleaner.higienizar_cpf)  # Limpeza de CPFs
            df[6] = df[6].apply(lambda x: DataCleaner.higienizar_cnpj(x) if pd.notna(x) else None)  # Limpeza de CNPJs
            df[7] = df[7].apply(lambda x: DataCleaner.higienizar_cnpj(x) if pd.notna(x) else None)  # Limpeza de CNPJs
            
            # Garantir que as colunas são do tipo numérico
            df = DataCleaner.garantir_tipo_numerico(df, [4, 5])
            
            # Validando CPFs e CNPJs
            df['CPF_VALIDO'] = df[0].apply(DataValidator.validar_cpf)
            df['CNPJ_LMF_VALIDO'] = df[6].apply(lambda x: DataValidator.validar_cnpj(x) if pd.notna(x) else None)
            df['CNPJ_LUC_VALIDO'] = df[7].apply(lambda x: DataValidator.validar_cnpj(x) if pd.notna(x) else None)
            
            # Ajustar os nomes das colunas
            df.columns = ["CPF", "PRIVATE", "INCOMPLETO", "DATA_ULTIMA_COMPRA", "TICKET_MEDIO", "TICKET_ULTIMA_COMPRA", "LOJA_MAIS_FREQUENTE", "LOJA_ULTIMA_COMPRA", "CPF_VALIDO", "CNPJ_LMF_VALIDO", "CNPJ_LUC_VALIDO"]     

            # Salvando em um csv temporário.
            df.to_csv(self.temp_file, index=False, header=False)
            print(f"Arquivo temporário {self.temp_file} criado com sucesso")

            # Usando COPY para carregar os dados no BD.
            with open(self.temp_file, 'r') as f:
                self.cursor.copy_expert("COPY base_teste FROM STDIN WITH CSV", f)
                print("Dados carregados com sucesso na tabela base_teste")
        except Exception as e:
            print(f"Erro ao carregar os dados {e}")      

    