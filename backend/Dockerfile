FROM python:3.11

RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=${PYTHONPATH}:/app

COPY . .

EXPOSE 8000

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main

COPY start.sh .

RUN chmod +x start.sh