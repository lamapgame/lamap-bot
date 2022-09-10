FROM python:3.10.6

RUN apt-get install libpq-dev

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py", "prod"]