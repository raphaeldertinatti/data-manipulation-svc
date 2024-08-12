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
cd data-manipulation-service
```
**Passo 2: Docker Compose**  
O projeto utiliza Docker Compose para orquestrar os serviços necessários. O arquivo docker-compose.yml define três serviços:

- **db:** Um container com PostgreSQL que armazena os dados.  
- **adminer:** Uma interface web para gerenciar o banco de dados PostgreSQL e visualizar as tabelas.  
- **data_loader:** Um container que executa o script principal (main.py) para carregar e processar os dados.
  
Para construir e executar os serviços, use o comando:  
```
docker-compose up --build
```
Isso irá:  

Configurar o banco de dados PostgreSQL.  
Executar o script SQL (init.sql) para criar a tabela que receberá a carga de dados no banco.  
Executar o serviço de carregamento de dados.  

**Passo 4: Acessar a Interface Adminer**
Após executar o Docker Compose, a interface Adminer estará disponível em [http://localhost:8080](http://localhost:8080).  
Use as credenciais abaixo para acessar o banco de dados:  

- **SGBD**: Postgres  
- **User**: Postgres  
- **Password**: Postgres
- **Database**: db_clientes

