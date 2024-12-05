from src.app.extract.extractor import Extractor
from src.common.const import INSIGHTS_TABLE_NAME
import seaborn as sns
import matplotlib.pyplot as plt
import os


class Visualizer(object):
    def __init__(self):
        self.extractor = Extractor()

    def create_graphs(self):
        self._run_first_graph()
        self._run_second_graph()
        
    def _run_first_graph(self):
        query = self._get_first_graph_query()

        first_df = self.extractor.extract_data_from_postgres_as_df(query)
        self._create_first_graph(first_df)

    def _run_second_graph(self):
        query = self._get_second_graph_query()

        second_df = self.extractor.extract_data_from_postgres_as_df(query)
        self._create_second_graph(second_df)

    def _get_first_graph_query(self):
        query = f"""
            SELECT 
                origin,
                airline,
                SUM(average_delay * amount_of_times_flew) / SUM(amount_of_times_flew) AS weighted_average_delay
            FROM {INSIGHTS_TABLE_NAME}
            GROUP BY origin, airline;
            """

        return query
    
    def _get_second_graph_query(self):
        query = f"""
            SELECT
                origin,
                airline,
                flight_number,
                cancellation_chance
            FROM {INSIGHTS_TABLE_NAME}
            ORDER BY cancellation_chance DESC;
            """

        return query
    
    def _create_first_graph(self, df):
        print('Creating first graph...')
        origin_chunks = [df['origin'].unique()[i:i+50] for i in range(0, len(df['origin'].unique()), 30)]

        for idx, chunk in enumerate(origin_chunks):
            chunk_df = df[df['origin'].isin(chunk)]
            plt.figure(figsize=(15, 7))
            sns.barplot(data=chunk_df, x="origin", y="weighted_average_delay", hue="airline")
            plt.xticks(rotation=45)
            plt.title(f"Média Ponderada de Atraso (Origens {idx*50 + 1} a {(idx+1)*50})")

            output_dir = "./first_graph"
            os.makedirs(output_dir, exist_ok=True)

            plt.savefig(f"{output_dir}/delay_chart_chunk_{idx+1}.pdf")
            plt.close()
    
    def _create_second_graph(self, df):
        print('Creating second graph...')
        
        origin_chunks = [df['origin'].unique()[i:i+25] for i in range(0, len(df['origin'].unique()), 25)]
        
        for idx, chunk in enumerate(origin_chunks):
            chunk_df = df[df['origin'].isin(chunk)]
            
            top_flight_numbers = chunk_df['flight_number'].value_counts().head(20).index
            chunk_df = chunk_df[chunk_df['flight_number'].isin(top_flight_numbers)]
            
            plt.figure(figsize=(18, 10))
            sns.scatterplot(
                data=chunk_df, 
                x="origin", 
                y="airline", 
                hue="flight_number", 
                size="cancellation_chance", 
                palette="tab20", 
                sizes=(50, 500)  
            )
            
            plt.xlabel("Origem")
            plt.ylabel("Linha Aérea")
            plt.title("Gráfico de Pontos: Origem vs Linha Aérea")
            
            plt.legend(
                title="Legenda",
                bbox_to_anchor=(1.05, 1), 
                loc='upper left',
                borderaxespad=0,
                fontsize='small'
            )
            
            plt.xticks(rotation=90)
            
            output_dir = "./second_graph"
            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(f"{output_dir}/cancellation_chance_chart_chunk_{idx+1}.pdf", bbox_inches='tight')
            plt.close()
