# Biblioteca de expressão regular (regex) e pandas.
import re
import pandas as pd

# Classe para limpeza de dados
class DataCleaner:
    # Método estático limpeza CPF
    @staticmethod
    def higienizar_cpf(cpf):
        return re.sub(r'\D','',cpf) 
    # Método estático limpeza CNPJ
    @staticmethod
    def higienizar_cnpj(cnpj):
        return re.sub(r'\D','',cnpj)
    # Método estático padroniza campo numérico para Banco de Dados
    @staticmethod
    def garantir_tipo_numerico(df, colunas):        
        for coluna in colunas:
            df[coluna] = df[coluna].astype(str).str.replace(',', '.')
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
        return df
    # Substitui ocorrências da string 'NULL' por '' em todo o DataFrame.
    @staticmethod
    def substituir_null_por_vazio(df):        
        return df.replace('NULL', '')