import logging
from hashlib import md5
from typing import Any, Dict

from celery import Celery
from src.settings import get_celery_settings

logger = logging.getLogger(__name__)
settings = get_celery_settings()


app = Celery(
    settings.worker_name,
    backend=settings.redis_celery_uri,
    broker=settings.rabbitmq_uri,
)

app.conf.task_routes = {"compute_hash_by_file": {"queue": settings.celery_queue_name}}

app.conf.update(task_track_started=True)


@app.task(acks_late=True, name="compute_hash_by_file", bind=True)
def compute_hash_by_file(self, file, hash_type: str = "md5") -> Dict[str, Any]:
    return {"hash": md5(file.encode("utf-8")).hexdigest()}
