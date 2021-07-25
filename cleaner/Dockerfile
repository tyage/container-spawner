# install deps
FROM python:3.9-alpine as build

RUN pip install pipenv

WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN sh -c 'PIPENV_VENV_IN_PROJECT=1 pipenv install'

# run app
FROM docker:dind

WORKDIR /app
COPY --from=build /app /app/
COPY --from=build /usr/local/bin/ /usr/local/bin/
COPY --from=build /usr/local/include/ /usr/local/include/
COPY --from=build /usr/local/lib/ /usr/local/lib/
COPY --from=build /usr/lib/ /usr/local/lib/
COPY . /app/

RUN /app/.venv/bin/pip3 install six

CMD .venv/bin/python -mapp.py
