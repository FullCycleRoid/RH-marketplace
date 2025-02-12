#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    celery --app=src.core.celery.celery_app:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
    celery --app=src.core.celery.celery_app:celery flower --basic_auth=21yard:TjLbUqULUddH
elif [[ "${1}" == "beat" ]]; then
    celery --app=src.core.celery.celery_app:celery beat -l INFO
fi