FROM python:3.11.9-slim-bookworm

RUN apt-get update && \
    apt-get install -y gcc libpq-dev python3-cffi libcairo2 libcairo2-dev libpango-1.0-0 libpango1.0-dev libpangocairo-1.0-0 libgdk-pixbuf2.0-0 && \
    apt clean && \
    rm -rf /var/cache/apt/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

COPY requirements/ /tmp/requirements

RUN pip install -U pip && \
    pip install --no-cache-dir -r /tmp/requirements/dev.txt

COPY . /src
ENV PATH "$PATH:/src/scripts"

RUN chmod +x /src/scripts/*

WORKDIR /src
