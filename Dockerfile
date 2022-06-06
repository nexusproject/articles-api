FROM python:3.9-slim-buster
LABEL maintainer = "Dmitry Sergeev <realnexusway@gmail.com>"

# Dependencies
RUN pip install --upgrade pip && \
    apt update && apt install -y make curl && \
    curl -fsSL -o /usr/local/bin/dbmate \
    https://github.com/amacneil/dbmate/releases/download/v1.7.0/dbmate-linux-amd64 && \
    chmod +x /usr/local/bin/dbmate && \
    pip install poetry

RUN poetry config

WORKDIR /articles-api
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-interaction --no-ansi

COPY . .
COPY Makefile .
ENTRYPOINT ["/usr/bin/make"]

