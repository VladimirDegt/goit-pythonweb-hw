FROM python:3.11-alpine

ENV APP_HOME=/app

WORKDIR $APP_HOME

# Встановлюємо системні пакети, які потрібні для компіляції psycopg2
RUN apk add --no-cache gcc musl-dev postgresql-dev libpq

COPY poetry.lock $APP_HOME/poetry.lock
COPY pyproject.toml $APP_HOME/pyproject.toml

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --only main

COPY goit-pythonweb-hw-02/ .

EXPOSE 8000

CMD ["python", "main.py"]