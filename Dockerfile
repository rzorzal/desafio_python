FROM --platform=linux/amd64 python:3.11.10

RUN apt-get update && apt-get install -y gcc unixodbc-dev gpg


# INSTALL POETRY 
RUN pip install poetry

WORKDIR /code
COPY ./pyproject.toml ./poetry.lock*  /code/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . .
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]