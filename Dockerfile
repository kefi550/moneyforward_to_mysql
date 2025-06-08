FROM python:3.12-slim-bookworm AS export
RUN pip install --no-cache-dir pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv requirements > /requirements.lock

FROM python:3.12-slim-bookworm AS builder
COPY --from=export /requirements.lock /
RUN apt-get update && apt-get install -y \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r /requirements.lock

FROM python:3.12-slim-bookworm AS runner
WORKDIR /app
COPY ./src/upsert_cashflows.py ./src/upsert_cashflows.py
COPY ./src/db.py ./src/db.py
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
ENTRYPOINT ["python", "src/upsert_cashflows.py"]
