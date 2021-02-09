FROM python:3.8.5-slim

WORKDIR /app/

ADD . /app
EXPOSE 5000

RUN pip install -r requirements.txt