# Data Manipulation Service
## Serviço de manipulação e persistência de dados em um banco de dados relacional.
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

### Visão Geral
Este projeto é um serviço de manipulação de dados e persistência em um banco de dados relacional (PostgreSQL), desenvolvido em Python. O serviço recebe um arquivo TXT como entrada, persiste os dados em um banco de dados, realiza higienização, valida CPFs/CNPJs e é totalmente containerizado usando Docker.


### Pré-requisitos

Certifique-se de ter a seguintes ferramentas instaladas:

- [Docker Desktop](https://www.docker.com/get-started)   
  ou  
- [Docker Engine](https://docs.docker.com/engine/install/)

### Configuração e Execução

**Passo 1: Clonar o Repositório**  
Clone este repositório para a sua máquina local:

```
git clone https://github.com/raphaeldertinatti/data-manipulation-svc.git
```
**Passo 2: Docker Compose**  
O projeto utiliza Docker Compose para orquestrar os serviços necessários. O arquivo docker-compose.yml define três serviços:

- **db:** Um container com PostgreSQL que armazena os dados.  
- **adminer:** Uma interface web para gerenciar o banco de dados PostgreSQL e visualizar as tabelas.  
- **data_loader:** Um container que executa o script principal (main.py) para carregar e processar os dados.
  
Para construir e executar os serviços, use o comando abaixo:  
obs (esteja dentro da pasta do repositório, na mesma pasta do arquivo docker-compose.yml, o Docker Desktop deve estar aberto (Windows) ou Docker Engine instalado e com o serviço inicializado (Linux)):  
```
cd data-manipulation-service
docker-compose up --build
```
Isso irá:  

Configurar o banco de dados PostgreSQL.  
Executar o script SQL (init.sql) para criar a tabela que receberá a carga de dados no banco.  
Executar o serviço de carregamento de dados.  

**Passo 3: Acessar a Interface Adminer**  
Após executar o Docker Compose, a interface Adminer estará disponível em [http://localhost:8080](http://localhost:8080).  
Use as credenciais abaixo para acessar o banco de dados:  

- **Sistema**: PostgreSQL
- **Servidor**: db  
- **User**: postgres  
- **Password**: postgres
- **Database**: db_clientes

Nesta interface você poderá verificar a tabela criada e como ficaram a disposição dos dados após carga.

### Descrição dos Componentes
**app/data_cleaner.py**  
Este script contém funções para higienização de dados removendo caracteres não numéricos dos campos contendo CPF e CNPJ, substituindo a palavra NULL por uma string vazia, além de garantir que colunas numéricas sejam corretamente formatadas, substituindo as vírgulas por ponto, conforme padrão do SGBD.

**app/data_loader.py**  
O script principal para realização da carga de dados do arquivo de texto para o banco de dados. Ele utiliza o data_cleaner para limpar os dados e o data_validator para validar os campos de CPF e CNPJ antes de carregá-los.

**app/data_validator.py**  
Fornece funções para validar CPFs e CNPJs usando a biblioteca [validate-docbr](https://pypi.org/project/validate-docbr/).

**app/db_connector.py**  
Contém a classe DBConnector, responsável por gerenciar a conexão com o banco de dados PostgreSQL.  

**main.py**  
Script que coordena a execução do serviço, desde a conexão com o banco de dados até a execução do carregamento de dados.

## Dependências
O projeto utiliza as seguintes bibliotecas, conforme arquivo requirements.txt:  
- **[psycopg2-binary](https://pypi.org/project/psycopg2-binary/)** (conexão de aplicações Python com bancos de dados PostgreSQL)
- **[sqlalchemy](https://pypi.org/project/SQLAlchemy/)** (permite interagir com bancos de dados relacionais usando objetos Python)
- **[pandas](https://pypi.org/project/pandas/)** (manipulação e análise de dados em Python)
- **[regex](https://pypi.org/project/regex/)** (expressões regulares, uma ferramenta poderosa para encontrar padrões em texto)
- **[validate-docbr](https://pypi.org/project/validate-docbr/)** (específica para a validação de documentos brasileiros, como CPF, CNPJ, RG e outros.)
- **[pytest](https://pypi.org/project/pytest/)**: (execução de testes automatizados).

## Execução do Serviço
O serviço desenvolvido realiza um processo manipulação de dados que inclui as seguintes etapas:  

- **Limpeza dos Dados:**  
Os dados são submetidos a um processo de limpeza, onde CPFs e CNPJs são normalizados removendo caracteres especiais. Isso garante que as informações estejam em um formato consistente para processamento. Todas as ocorrências de 'NULL' nas colunas do dataset são substituídas por strings vazias, evitando erros durante a carga no banco de dados.

- **Validação dos Dados:**  
Após a limpeza, o serviço valida os valores de CPF e CNPJ usando as bibliotecas especializadas validate-docbr. Três novas colunas são adicionadas ao dataset para armazenar os resultados da validação:  
**CPF_VALIDO:** Indica se o CPF fornecido é válido (True) ou inválido (False).  
**CNPJ_LMF_VALIDO:** Indica se o CNPJ da loja mais frequente é válido (True) ou inválido (False).  
**CNPJ_LUC_VALIDO:** Indica se o CNPJ da loja da última compra é válido (True) ou inválido (False).  
  
- **Carga dos Dados:**  
Após o processo de limpeza e validação, os dados são carregados na tabela base_teste do banco de dados PostgreSQL usando o comando COPY. O serviço então confirma as alterações no banco, garantindo a integridade dos dados carregados.

## Testes Automatizados com Pytest
Este projeto utiliza o pytest para a execução de testes automatizados. Os testes foram configurados para validar as funcionalidades principais do projeto, incluindo a limpeza e validação de dados.
Além disso, o projeto está em integração contínua com o Github Actions, validando e realizando os testes a cada pull ou push request.


