#!/usr/bin/env bash

set -e

DEFAULT_MODULE_NAME=src.main

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-info}
LOG_CONFIG=${LOG_CONFIG:-/src/logging.ini}

SSL_CERT_FILE=/etc/ssl/certs/21yardcom.crt
SSL_KEY_FILE=/etc/ssl/certs/key.pem


if [[ -f "$SSL_CERT_FILE" ]] && [[ -f "$SSL_KEY_FILE" ]]; then
  echo "START ENCRYPTED HTTPS INSTANCE"
  exec uvicorn --reload --proxy-headers --host $HOST --port $PORT --log-config $LOG_CONFIG --ssl-certfile "$SSL_CERT_FILE" --ssl-keyfile "$SSL_KEY_FILE" "$APP_MODULE"
else
  echo "START UNENCRYPTED HTTP INSTANCE"
  exec uvicorn --reload --proxy-headers --host $HOST --port $PORT --log-config $LOG_CONFIG "$APP_MODULE"
fi