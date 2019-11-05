FROM python:3.7
LABEL maintainer "Julius Rajala <juliusrajala@gmail.com>"

RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pipenv install --dev
