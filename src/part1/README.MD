1. Registry in Kaggle
2. Create a Token API in Kaggle platform
3. Configure JSON token in user home ~/.kaggle/kaggle.json
4. Run python script "download-dadtasets.py" for downdload CSV files or by use CLI "kaggle datasets download -d 'yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018'"
5. Create a new folder ./csv
6. Extraction "airline-delay-and-cancellation-data-2009-2018.zip" to ./csv and deletion of the "airline-delay-and-cancellation-data-2009-2018.zip" file.
7. Create YML database file for docker-compose - Retional Database
8. Create python script for ingestion in database with creation of the new collumns.


Definir todos as colunas para o tipo texto.
Adicionar dados default a coluna da tabela se não informado. 
Tratar dados do tipo vazio antes de inserir no banco para valor default.