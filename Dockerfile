FROM python:3.11-slim-buster

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
