FROM python:3.11.4-slim

RUN apt-get install -y libpq-dev
WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN pip install -U pip poetry
RUN poetry install --no-root --only main

COPY ./ ./

CMD ["python", "bot.py", "prod"]
