import logging
from functools import lru_cache

from pydantic import BaseSettings, Field

logger = logging.getLogger(__name__)


class RabbitMQSettings(BaseSettings):
    rabbitmq_host: str = Field(env="RABBITMQ_HOST", default="rabbitmq")
    rabbitmq_username: str = Field(env="RABBITMQ_USERNAME", default="user")
    rabbitmq_password: str = Field(env="RABBITMQ_PASSWORD", default="bitnami")
    rabbitmq_port: str = Field(env="RABBITMQ_PORT", default="5672")

    @property
    def rabbitmq_uri(self) -> str:
        return f"amqp://{self.rabbitmq_username}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}//"


class RedisSettings(BaseSettings):
    redis_host: str = Field(env="REDIS_HOST", default="redis")
    redis_username: str = Field(env="REDIS_USERNAME", default="")
    redis_password: str = Field(env="REDIS_PASSWORD", default="password123")
    redis_port: str = Field(env="REDIS_PORT", default="6379")

    redis_celery_db_index: str = Field(env="REDIS_CELERY_DB_INDEX", default="0")
    redis_store_db_index: str = Field(env="REDIS_STORE_DB_INDEX", default="1")

    @property
    def _base_redis_uri(self) -> str:
        return f"redis://{self.redis_username}:{self.redis_password}@{self.redis_host}:{self.redis_port}"

    @property
    def redis_celery_uri(self) -> str:
        return f"{self._base_redis_uri}/{self.redis_celery_db_index}"

    @property
    def redis_store_uri(self) -> str:
        return f"{self._base_redis_uri}/{self.redis_store_db_index}"


class CelerySettings(RedisSettings, RabbitMQSettings):
    worker_name: str = "celery_worker"
    celery_queue_name: str = "test-queue"
    logs_file_path: str = "./logs/celery.log"


@lru_cache
def get_celery_settings() -> CelerySettings:
    logger.info("Loading config settings from the environment...")
    return CelerySettings()
