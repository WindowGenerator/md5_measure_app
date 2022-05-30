import logging

from functools import lru_cache
from typing import Any, Dict, List

from pydantic import BaseSettings, Field


logger = logging.getLogger(__name__)


class FastApiInitSettings(BaseSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "Hash Measure App"
    version: str = "0.0.1"

    @property
    def fastapi_init_args(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }


class PostgresSettings(BaseSettings):
    pg_user: str = Field(env="POSTGRES_USER", default="postgres")
    pg_pass: str = Field(env="POSTGRES_PASSWORD", default="secret")
    pg_host: str = Field(env="POSTGRES_HOST", default="postgres")
    pg_database: str = Field(env="POSTGRES_DB", default="hash_record_db")

    @property
    def asyncpg_url(self) -> str:
        return f"postgresql+asyncpg://{self.pg_user}:{self.pg_pass}@{self.pg_host}:5432/{self.pg_database}"

    min_connection_count: int = 1
    max_connection_count: int = 10


class RabbitMQSettings(BaseSettings):
    rabbitmq_host: str = Field(env="RABBITMQ_HOST", default="rabbitmq")
    rabbitmq_username: str = Field(env="RABBITMQ_USERNAME", default="user")
    rabbitmq_password: str = Field(env="RABBITMQ_PASSWORD", default="bitnami")
    rabbitmq_port: str = Field(env="RABBITMQ_PORT", default="5672")

    @property
    def rabbitmq_uri(self) -> str:
        return f"amqp://{self.rabbitmq_username}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}"


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


class AppSettings(FastApiInitSettings, PostgresSettings, CelerySettings):
    api_prefix: str = "/api/v1"
    allowed_hosts: List[str] = ["*"]

    logging_level: int = logging.INFO

    class Config:
        validate_assignment = True


@lru_cache
def get_app_settings() -> AppSettings:
    logger.info("Loading config settings from the environment...")
    return AppSettings()


@lru_cache
def get_celery_settings() -> CelerySettings:
    logger.info("Loading config settings from the environment...")
    return CelerySettings()
