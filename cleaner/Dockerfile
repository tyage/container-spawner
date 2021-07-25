FROM python:3.9-alpine

RUN pip install pipenv

WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN sh -c 'PIPENV_VENV_IN_PROJECT=1 pipenv install'

COPY . /app/

CMD .venv/bin/python cli.py
