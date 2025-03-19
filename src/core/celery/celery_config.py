from kombu import Exchange, Queue

from src.core.cache.redis.client import REDIS_URL


class Config:
    broker_url = f"{REDIS_URL}"
    include = ["src.tasks.tasks"]

    timezone = "UTC"
    enable_utc = True
    task_serializer = "json"
    accept_content = ["json"]
    result_serializer = "json"

    task_default_queue = "celery_queue"
    task_queues = (
        Queue("celery_queue", Exchange("celery_queue"), routing_key="celery_queue"),
    )

    beat_schedule = {}
