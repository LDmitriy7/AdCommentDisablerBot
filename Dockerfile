FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml pdm.lock ./

RUN pip install pdm && pdm install

COPY . .

CMD pdm run python src