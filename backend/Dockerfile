FROM python:3.10-slim
ARG POETRY_PARAMS=""
ENV PYTHONUNBUFFERED=1
ENV PATH="${PATH}:/root/.local/bin"
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN apt update && apt install curl -y
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml /app/

RUN poetry install --no-interaction

COPY . .

