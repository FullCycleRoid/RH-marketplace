#!/usr/bin/env bash

set -e

DEFAULT_MODULE_NAME=src.main

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

DEFAULT_GUNICORN_CONF=/src/gunicorn/gunicorn_conf.py
export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}
export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}

SSL_CERT_FILE=/etc/ssl/certs/21yardcom.crt
SSL_KEY_FILE=/etc/ssl/certs/key.pem


if [[ -f "$SSL_CERT_FILE" ]] && [[ -f "$SSL_KEY_FILE" ]]; then
  echo "START ENCRYPTED HTTPS INSTANCE"
  gunicorn --bind "$HOST":"$PORT" -k "$WORKER_CLASS" -c "$GUNICORN_CONF" --certfile "$SSL_CERT_FILE" --keyfile "$SSL_KEY_FILE" "$APP_MODULE"
else
  echo "START UNENCRYPTED HTTP INSTANCE"
  gunicorn  --bind "$HOST":"$PORT" -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE"
fi
