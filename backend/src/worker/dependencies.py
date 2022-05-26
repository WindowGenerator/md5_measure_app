from fastapi import Request
from src.worker.celery_api import CeleryApi


async def get_celery_api(request: Request) -> CeleryApi:
    return request.app.state.celery
