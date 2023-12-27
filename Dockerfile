FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Poetry
RUN pip install poetry

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev

# Railway will define environment variables for you

# Run bot.py when the container launches
CMD ["python", "bot.py"]