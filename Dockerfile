FROM python:3.8.5-slim

# set working directory to /app/
WORKDIR /app/

ADD . /app
EXPOSE 5000

# install python dependencies
RUN pip install -r requirements.txt