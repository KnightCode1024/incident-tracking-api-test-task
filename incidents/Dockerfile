FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
WORKDIR /app/www/incidents
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .