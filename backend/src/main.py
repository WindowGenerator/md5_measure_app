from typing import Callable

from fastapi import FastAPI
from src.db.events import close_db_connection, connect_to_db
from src.handlers import router as api_router
from src.settings import AppSettings, get_app_settings, get_celery_settings
from src.worker.celery_api import CeleryApi


def _create_start_app_handler(
    app: FastAPI,
    settings: AppSettings,
) -> Callable:  # type: ignore
    async def start_app() -> None:
        celery_settings = get_celery_settings()
        app.state.celery = CeleryApi(celery_settings)

        await connect_to_db(app, settings)

    return start_app


def _create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def stop_app() -> None:
        pass
        await close_db_connection(app)

    return stop_app


def create_app() -> FastAPI:
    settings = get_app_settings()

    app = FastAPI(**settings.fastapi_init_args)

    app.include_router(api_router, prefix=settings.api_prefix)

    app.add_event_handler(
        "startup",
        _create_start_app_handler(app, settings),
    )
    app.add_event_handler(
        "shutdown",
        _create_stop_app_handler(app),
    )

    return app
