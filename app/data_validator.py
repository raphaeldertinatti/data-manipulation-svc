# Biblioteca de Validação 
from validate_docbr import CPF, CNPJ

#Classe para validação de CPF/CNPJ
class DataValidator:
    # Método estático validação de CPF
    @staticmethod
    def validar_cpf(cpf):        
        cpf_obj = CPF()
        return cpf_obj.validate(cpf)
    # Método estático validação de CNPJ
    @staticmethod
    def validar_cnpj(cnpj):        
        cnpj_obj = CNPJ()
        return cnpj_obj.validate(cnpj)