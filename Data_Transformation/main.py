import sys
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import accuracy_score
from tqdm import tqdm

# Definir o caminho do banco de dados SQLite
project_root = os.path.dirname(os.path.dirname(os.path.abspath('')))
db_path = os.path.join(project_root, 'Python\passageiros\desafio_python\data', 'airline_data.db')

# Verificar se o arquivo do banco de dados existe
if not os.path.exists(db_path):
    raise FileNotFoundError(f"O arquivo do banco de dados não foi encontrado em: {db_path}")

# Criar conexão com banco de dados (SQLite)
print("Criando conexão com o banco de dados SQLite...")
engine = create_engine(f'sqlite:///{db_path}')

print("Criando sessão...")
Session = sessionmaker(bind=engine)
session = Session()

# Carregar os dados da tabela 'Base' em blocos, pois ao tentar de forma única a memória estorou!
print("Carregando dados da tabela 'Base' em blocos...")
chunksize = 90000
chunks = pd.read_sql_query("SELECT * FROM Base", engine, chunksize=chunksize)

flight_insights_list = []

for chunk in tqdm(chunks, desc="Processando blocos de dados"):
    if chunk.empty:
        continue
    
    # Criar o DataFrame 'flight_insights' para o bloco atual com base nos critéios
    flight_insights_chunk = chunk.groupby(['OP_CARRIER', 'OP_CARRIER_FL_NUM', 'ORIGIN']).agg(
        avg_delay=('CARRIER_DELAY', 'mean'),
        weather_delay=('WEATHER_DELAY', 'mean'),
        nas_delay=('NAS_DELAY', 'mean'),
        security_delay=('SECURITY_DELAY', 'mean'),
        late_aircraft_delay=('LATE_AIRCRAFT_DELAY', 'mean'),
        total_air_time=('AIR_TIME', 'sum')
    ).reset_index()
    
    # Calcular a média de tempo de delay somando os delays individuais
    flight_insights_chunk['avg_delay'] = (
        flight_insights_chunk['avg_delay'] +
        flight_insights_chunk['weather_delay'] +
        flight_insights_chunk['nas_delay'] +
        flight_insights_chunk['security_delay'] +
        flight_insights_chunk['late_aircraft_delay']
    )
    
    # Remover colunas intermediárias de delay
    flight_insights_chunk.drop(columns=['weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay'], inplace=True)
    
    flight_insights_list.append(flight_insights_chunk)

# Verificar se há dados para concatenar
if not flight_insights_list:
    print("Nenhum dado para concatenar")

# Concatenar todos os blocos processados
flight_insights = pd.concat(flight_insights_list, ignore_index=True)

# Preparar os dados para o modelo de previsão de cancelamento
print("Preparando dados para o modelo de previsão de cancelamento...")
df_chunks = pd.read_sql_query("SELECT * FROM Base", engine, chunksize=chunksize)

# Inicializar o modelo de regressão logística com treinamento incremental
model = SGDClassifier(loss='log_loss', max_iter=1000, tol=1e-3)

for chunk in tqdm(df_chunks, desc="Treinando o modelo com blocos de dados"):
    if chunk.empty:
        continue
    
    chunk['CANCELLED'] = chunk['CANCELLED'].astype(int)
    X_chunk = chunk[['CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']]
    y_chunk = chunk['CANCELLED']
    
    model.partial_fit(X_chunk, y_chunk, classes=np.array([0, 1]))

# Avaliar o modelo em blocos menores para evitar problemas de memória
print("Avaliando o modelo...")
accuracy_list = []
for chunk in tqdm(pd.read_sql_query("SELECT * FROM Base", engine, chunksize=chunksize), desc="Avaliando o modelo com blocos de dados"):
    if chunk.empty:
        continue
    
    X_chunk = chunk[['CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']]
    y_chunk = chunk['CANCELLED']
    
    y_pred_chunk = model.predict(X_chunk)
    accuracy_list.append(accuracy_score(y_chunk, y_pred_chunk))

# Calcular a precisão média do modelo
accuracy = np.mean(accuracy_list)
print(f"Model Accuracy: {accuracy}")

# Prever a probabilidade de cancelamento para cada voo no DataFrame 'flight_insights' em blocos menores para evitar problemas de memória
print("Prevendo a probabilidade de cancelamento para cada voo no DataFrame 'flight_insights'...")
cancel_prob_list = []
for chunk in tqdm(np.array_split(flight_insights[['avg_delay']], 1000), desc="Prevendo cancelamentos"):
    # Criar um DataFrame temporário com as mesmas colunas usadas no treinamento do modelo e preencher com zeros
    temp_df = pd.DataFrame(0, index=np.arange(len(chunk)), columns=['CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY'])
    
    # Preencher a coluna 'CARRIER_DELAY' com os valores do chunk atual
    temp_df['CARRIER_DELAY'] = chunk.values.flatten()
    
    # Prever a probabilidade de cancelamento usando o modelo treinado
    cancel_prob_chunk = model.predict_proba(temp_df)[:, 1]
    
    cancel_prob_list.append(cancel_prob_chunk)

flight_insights['cancel_prob'] = np.concatenate(cancel_prob_list)

# Salvar o DataFrame 'flight_insights' em uma nova tabela no banco de dados SQLite
print("Salvando o DataFrame 'flight_insights' em uma nova tabela no banco de dados SQLite...")
flight_insights.to_sql('flight_insights', engine, if_exists='replace', index=False)

print("A tabela 'flight_insights' foi criada e salva no banco de dados SQLite.")

print("Encerrando execução do script.")
sys.exit() #Por alguma razão que não entendi tive que usar este comando para encerrar a aplicação pois a mesma não finalizava ao fim do script 