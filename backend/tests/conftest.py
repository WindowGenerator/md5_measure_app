import uuid

from dataclasses import dataclass
from typing import BinaryIO, Dict, Optional

import pytest

import pytest_asyncio

from celery.states import PENDING
from fastapi import Depends, FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.dependencies import get_files_hash_record_repository
from src.main import create_app
from src.schemas.files import Task as TaskSchema
from src.worker.dependencies import get_celery_api
from starlette.testclient import TestClient


@dataclass
class CeleryTask:
    id: str
    state: str
    result: Optional[Dict]


class TestCeleryApi:
    def compute_hash_by_file(self, file: str, hash_type: str) -> CeleryTask:
        return CeleryTask(id=str(uuid.uuid4()), state=PENDING, result=None)

    def set_task_state(
        self, task_id: str, state: str = PENDING, result: Optional[Dict] = None
    ) -> None:
        self._task = CeleryTask(id=task_id, state=state, result=result)
        return self._task

    def get_task(self, task_id: str) -> CeleryTask:
        return self._task


class TestFilesHashRecordRepository:
    def __init__(self) -> None:
        self._tasks: Dict[str, TaskSchema] = {}

    def init_tasks(self, tasks: Dict[str, TaskSchema]) -> None:
        self._tasks.update(tasks)

    async def get_hash_record(self, task_id: str) -> TaskSchema:
        return self._tasks[task_id]

    async def create_hash_record(
        self,
        task_id: str,
        hash_type: str,
        status: str = PENDING,
        result: str = "",
        hash_value: Optional[str] = None,
    ) -> TaskSchema:
        self._tasks[task_id] = TaskSchema(
            task_id=task_id,
            hash_type=hash_type,
            status=status,
            result=result,
            hash_value=hash_value,
        )

        return self._tasks[task_id]

    async def update_hash_record(
        self,
        task_id: str,
        status: str = PENDING,
        result: str = "",
        hash_value: Optional[str] = None,
    ) -> TaskSchema:

        self._tasks[task_id].status = status
        self._tasks[task_id].result = result
        self._tasks[task_id].hash_value = hash_value

        return self._tasks[task_id]


def _get_celery_api_mock(request: Request):
    return request.app.state.celery_api


async def _get_session_mock(request: Request):
    return None


def _get_files_hash_record_repository_mock(
    request: Request, session: AsyncSession = Depends(_get_session_mock)
):
    return request.app.state.repo_mock


@pytest_asyncio.fixture
async def get_files_hash_record_repository_mock(
    test_app: TestClient,
) -> TestFilesHashRecordRepository:
    return test_app.app.state.repo_mock


@pytest_asyncio.fixture
async def get_celery_api_mock(test_app: TestClient) -> TestFilesHashRecordRepository:
    return test_app.app.state.celery_api


@pytest.fixture(scope="function")
def test_app() -> FastAPI:
    app: FastAPI = create_app()
    client = TestClient(app)

    app.state.repo_mock = TestFilesHashRecordRepository()
    app.state.celery_api = TestCeleryApi()

    app.dependency_overrides[get_celery_api] = _get_celery_api_mock
    app.dependency_overrides[
        get_files_hash_record_repository
    ] = _get_files_hash_record_repository_mock

    yield client


@pytest.fixture
def simple_upload_file() -> BinaryIO:
    with open("./tests/data/dummy_file.txt", "rb") as fd:
        yield fd
