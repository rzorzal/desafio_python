<center>
  <h1> Desafio Python - Marcelo Viana Almeida </h1>
</center>

## Instrodução

Este desafio de programação em Python tem como objetivo realizar um ETL (extract, Transform, Load) com foco no tratamento de dados, criação, modelagem de banco de dados e codificação de funções para torná-lo adequado ao uso em contextos de Business Intelligence e comprir a proposta deste desafio. Este trabalho abrange desde a extração e transformação dos dados até sua carga final, garantindo a qualidade e a organização necessárias para gerar insights estratégicos propostos pelo desafio.

## Considerações iniciais:
- Arquivo Makefile não modificado conforme solicitado no <a href=README.original.md>README original</a>
- O Arrangue deste projeto é realizado pelo arquivo `index.py`, contido na raiz do repositório.
- Projeto estruturado com paradigma Orientado a Objetos
- Arquivo `index.py` contém funções que automatizam todo processo:
  - Donwload dos arquivos CSV
  - Extração do Zip
  - Mover para diretório de trabalho em src/part1/csv
  - Execução das migrations para criação da estrutura (tabelas e View) do banco de dados
  - Carregamento dos dados dos arquivos CSV no banco de dados
  - Geração e salvamento dos insights
- Todas as colunas na migração foram tipadas corretamente conforme tipo de colunas indentificado nos arquivos CSV
- Todos as dados de tuplas cuja natureza é vazio, foram tratados com valor default

## Instruções
- Instale as bibliotecas do projeto. Use `pip install -r requirements.txt`
- Renomei o arquivo `.env.example` para `.env` antes de executar o projeto


## Part 1 - Data Manupulation
Trata da construção de uma base de dados analítica local.
Nesta estapa foram utilizados biliotecas como:
Kaggle fonte de dados de treino e <i>machine learning</i>
- Kaggle:
  A interação com a plataforma Kaggle foi realizada por meio de API. Ao realizar o cadastro na plataforma Kaggle, foi gerado uma API-Token que configurada localmente, pode possibilitar o download programático dos arquivos CSV para montagem do banco de dados.

API-Token (json-token) aplicada em:

vim **~/.kaggle/kaggle.json**
```
{"username":"marcelovianaalmeida","key":"#EXAMPLE_KEY#"}
```

Com a API devidamente configurada é possível interagir com a API do Kaggle programaticamente ou via CLI.

**CLI:**
```
kaggle datasets download -d 'yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018'
```
**API:**
```
import kagglehub
path = kagglehub.dataset_download('yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018')
```

O uso da API é o mais indicado, uma vez que este simplifica o processo e reduz etapas de trabalho, como baixar e extrair os arquivos. Também foi possível incrementar outras funcionalidades ao uso do API para completar a operação alinhado com a necessidade deste projeto.


### Part 1 - Criação do serviço de banco de dados:
Foi escolhido o banco relacional `PostgreSQL`, por sua robustês e por ser um banco largamente utilizado para diversos tipos de demandas.
O arquivo `docker-compose.yml` localizado na raiz do projeto descreve os parâmetros de configuração e versão do banco de dados, a exemplo:

```
services:
  dcs-postgres:
    image: postgres:15.3-alpine
    container_name: dcs-postgres
    restart: always
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_USER: postgres
    ports:
      - 5432:5432
```

### Part 1 - Modelagem do banco

Foi utilizado para criação do modelo de dados duas bibliotecas; **sqlalchemy** e **alembic**.
O **sqlalchemy** é robusto e bem documentado, ele está sendo usado exclusivamente para ORM do projeto. Já o **alembic** é uma biblioteca auxiliar podedoza e prática para criação de Migrations (versionamento controlado de banco de dados).

### Tabelas

- Duas tabelas foram criadas para composição do projeto. 
- (**flight**) armazenar a massa de dados oriundos dos arquivos CSV.
- (**users_insights**) para armazenamento dos insights gerados na Part 2.
- Também foi criado uma **VIEW**  que faz a entrega de todas as informações necessárias para Part 2 e Part 3. O modivador principal foi reduzir linhas de código do lado da aplicação e deixar o máximo de processamento das **Queries** do lado do banco de dados.

 ## Part 2 - Data Transformation

**As responsabilidades de cálculos foram transferidas para o banco de dados.**

A view **data_transformation_view** foi criada para atender as demandas da Part 2 e também da Part 3.

Prévia da View:
```
# migrations/migrations/versions/86cdf44a8d6b_view_for_part2.py

select 
	item."OP_CARRIER",
	sum(item."CARRIER_DELAY") as "TOTAL_CARRIER_DELAY", 
	sum(item."WEATHER_DELAY") as "TOTAL_WEATHER_DELAY",
	sum(item."NAS_DELAY") as "TOTAL_NAS_DELAY",
	sum(item."SECURITY_DELAY") as "TOTAL_SECURITY_DELAY",
	sum(item."LATE_AIRCRAFT_DELAY") as "TOTAL_LATE_AIRCRAFT_DELAY",
	sum(item."AIR_TIME") as "TOTAL_AIR_TIME",
    ROUND(AVG(item."CARRIER_DELAY" + item."WEATHER_DELAY" + item."NAS_DELAY" + item."SECURITY_DELAY" + item."LATE_AIRCRAFT_DELAY")::numeric, 2) AS "DELAY_AVERAGE"
	from flight item 
	where item."CARRIER_DELAY" !=  'NaN'
	group by item."OP_CARRIER";
```

Este é o resultado da View, considerando a solicitação da Part 2:

```
OP_CARRIER:  9E, DELAY_AVERAGE: 51.32, TOTAL_AIR_TIME: 2671403
OP_CARRIER:  AA, DELAY_AVERAGE: 59.48, TOTAL_AIR_TIME: 16269001
OP_CARRIER:  AS, DELAY_AVERAGE: 45.68, TOTAL_AIR_TIME: 3163903
OP_CARRIER:  B6, DELAY_AVERAGE: 62.67, TOTAL_AIR_TIME: 5950518
OP_CARRIER:  CO, DELAY_AVERAGE: 55.79, TOTAL_AIR_TIME: 8453716
OP_CARRIER:  DL, DELAY_AVERAGE: 51.94, TOTAL_AIR_TIME: 10776100
OP_CARRIER:  EV, DELAY_AVERAGE: 58.96, TOTAL_AIR_TIME: 5192922
OP_CARRIER:  F9, DELAY_AVERAGE: 45.66, TOTAL_AIR_TIME: 2176193
OP_CARRIER:  FL, DELAY_AVERAGE: 54.50, TOTAL_AIR_TIME: 5862760
OP_CARRIER:  HA, DELAY_AVERAGE: 42.48, TOTAL_AIR_TIME: 1184797
OP_CARRIER:  MQ, DELAY_AVERAGE: 55.74, TOTAL_AIR_TIME: 6057045
OP_CARRIER:  NW, DELAY_AVERAGE: 48.63, TOTAL_AIR_TIME: 7334752
OP_CARRIER:  OH, DELAY_AVERAGE: 56.83, TOTAL_AIR_TIME: 3470770
OP_CARRIER:  OO, DELAY_AVERAGE: 53.91, TOTAL_AIR_TIME: 6538611
OP_CARRIER:  UA, DELAY_AVERAGE: 60.53, TOTAL_AIR_TIME: 9440570
OP_CARRIER:  US, DELAY_AVERAGE: 47.68, TOTAL_AIR_TIME: 9637345
OP_CARRIER:  WN, DELAY_AVERAGE: 47.27, TOTAL_AIR_TIME: 16567989
OP_CARRIER:  XE, DELAY_AVERAGE: 61.73, TOTAL_AIR_TIME: 5324301
OP_CARRIER:  YV, DELAY_AVERAGE: 61.43, TOTAL_AIR_TIME: 2872042
```
Este resultado é armazenado ao banco de dados controlado pela coluna de `created_at` para futuras análises.


Nota: 
Não pude concluir as a sololução que mostra a probabilidade de cancelamento de voos e também não pude fazer a Part 3.

