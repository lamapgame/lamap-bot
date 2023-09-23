FROM python:3.11.4-slim

RUN apt update && apt-get install -y libpq-dev postgresql-client --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get clean \
  && apt-get autoremove

WORKDIR /

COPY poetry.lock pyproject.toml ./
RUN pip install -U pip poetry
RUN poetry install

COPY ./ ./app

CMD ["python", "bot.py", "prod"]
