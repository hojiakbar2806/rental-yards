FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-root

COPY . /app/

EXPOSE 8000

CMD poetry run gunicorn main:app --workers=4 --worker-class=uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
