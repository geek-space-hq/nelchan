FROM python:3.9-slim as build

WORKDIR /usr/src/app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt > requirements.txt


FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY --from=build /usr/src/app/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD python cmd/prod.py