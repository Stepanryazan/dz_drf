FROM python:3.12

WORKDIR /app

RUN pip install --upgrade pip \
    && pip install poetry

COPY requirements.txt /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . /app/