FROM python:3.7
LABEL maintainer "Julius Rajala <juliusrajala@gmail.com>"

RUN apt-get update
RUN pip install pipenv

RUN mkdir /app
WORKDIR /app
COPY . /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install
EXPOSE 5000
