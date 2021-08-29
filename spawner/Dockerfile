FROM python:3.9-alpine

RUN pip install pipenv

WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN sh -c 'PIPENV_VENV_IN_PROJECT=1 pipenv install'

# workaround for the issue https://github.com/docker/docker-py/issues/2867
RUN /app/.venv/bin/pip3 install six

COPY . /app/

CMD .venv/bin/gunicorn -b :5000 app:app
