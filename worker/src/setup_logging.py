import logging

import redis
from celery.signals import after_setup_logger
from src.settings import get_celery_settings


class FileHandlerWithLocks(logging.FileHandler):
    """
    A handler that implements logging to a single file. in fact,
    a mechanism for sequential interaction of workers with file by means of locks
    """

    def __init__(self, filename, mode="a", encoding=None, delay=False):
        super().__init__(filename=filename, mode=mode, encoding=encoding, delay=delay)

        settings = get_celery_settings()
        self.__redis_client = redis.Redis.from_url(settings.redis_store_uri)

    def emit(self, record):
        """
        Emit a record.

        If the stream was not opened because 'delay' was specified in the
        constructor, open it before calling the superclass's emit.
        """
        with self.__redis_client.lock("logging_lock"):
            super().emit(record)


@after_setup_logger.connect
def setup_logging(logger, *args, **kwargs) -> None:
    settings = get_celery_settings()

    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = FileHandlerWithLocks(settings.logs_file_path)
    handler.setFormatter(fmt)
    logger.addHandler(handler)
