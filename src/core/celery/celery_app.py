from celery import Celery

from src.core.celery.celery_config import Config

celery = Celery("tasks")
celery.config_from_object(Config)
