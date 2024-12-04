import sys
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from pygame import mixer

# Definir o caminho do banco de dados SQLite
project_root = os.path.dirname(os.path.dirname(os.path.abspath('')))
db_path = os.path.join(project_root, 'Python\passageiros\desafio_python\data', 'airline_data.db')

# Verificar se o arquivo do banco de dados existe
if not os.path.exists(db_path):
    raise FileNotFoundError(f"O arquivo do banco de dados não foi encontrado em: {db_path}")

# Criar conexão com banco de dados (SQLite)
print("Criando conexão com o banco de dados SQLite...")
engine = create_engine(f'sqlite:///{db_path}')

# Carregar os dados da tabela 'flight_insights' para um DataFrame do pandas
print("Carregando dados da tabela 'flight_insights'...")
df = pd.read_sql_query("SELECT * FROM flight_insights", engine)

# Calcular a média de delay por origem e linha aérea
print("Calculando a média de delay por origem e linha aérea...")
df['frequenciaVoo'] = df.groupby(['OP_CARRIER', 'OP_CARRIER_FL_NUM', 'ORIGIN'])['avg_delay'].transform('count')
df['somaMediaVoo'] = df.groupby(['OP_CARRIER', 'OP_CARRIER_FL_NUM', 'ORIGIN'])['avg_delay'].transform('sum')
df['media_delay'] = df['somaMediaVoo'] / df['frequenciaVoo']

# Gráfico de barra: eixo X será a origem, eixo Y a média de delay e uma barra por linha aérea
print("Gerando gráfico de barra...")
plt.figure(figsize=(12, 8))
sns.barplot(x='ORIGIN', y='media_delay', hue='OP_CARRIER', data=df)
plt.title('Média de Delay por Origem e Linha Aérea')
plt.xlabel('Origem')
plt.ylabel('Média de Delay')
plt.legend(title='Linha Aérea')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('grafico_barra.png')
plt.show()

# Gráfico de pontos: eixo X a origem, eixo Y a linha aérea, cor o número do voo e tamanho a chance do voo ser cancelado
print("Gerando gráfico de pontos...")
plt.figure(figsize=(12, 8))
sns.scatterplot(x='ORIGIN', y='OP_CARRIER', hue='OP_CARRIER_FL_NUM', size='cancel_prob', data=df, palette='viridis', sizes=(20, 200))
plt.title('Chance de Cancelamento por Origem, Linha Aérea e Número do Voo')
plt.xlabel('Origem')
plt.ylabel('Linha Aérea')
plt.legend(title='Número do Voo', bbox_to_anchor=(1.05, 1), loc=2)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('grafico_pontos.png')
plt.show()

print("Encerrando execução do script.")
mixer.music.load('som.mp3')
mixer.music.play()
sys.exit()