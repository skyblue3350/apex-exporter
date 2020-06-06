FROM python:3-slim as builder

WORKDIR /opt/app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt > requirements.txt

FROM python:3-slim

WORKDIR /opt/app
COPY --from=builder /opt/app/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 9316
CMD python -m apex_exporter
