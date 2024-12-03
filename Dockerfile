FROM python:3.11

# Definir o diretório de trabalho no contêiner
WORKDIR /desafio_python


COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código do projeto
COPY . .

# Comando para rodar a aplicação
CMD ["python", "app.py"]