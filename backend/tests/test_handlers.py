import uuid

from typing import BinaryIO

import pytest

from celery.states import FAILURE, PENDING, SUCCESS
from fastapi.testclient import TestClient
from src.schemas.files import Task
from tests.conftest import TestCeleryApi, TestFilesHashRecordRepository


@pytest.mark.asyncio
async def test_simple_compute_hash(
    test_app: TestClient, simple_upload_file: BinaryIO
) -> None:
    response = test_app.post(
        "/api/v1/files/compute/hash", files={"upload_file": simple_upload_file}
    )
    print(response.json())
    assert response.status_code == 201

    body = response.json()

    assert "task_id" in body
    assert str(uuid.UUID(body["task_id"])) == body["task_id"]


@pytest.mark.asyncio
async def test_simple_get_computed_hash(
    test_app: TestClient,
    get_files_hash_record_repository_mock: TestFilesHashRecordRepository,
    get_celery_api_mock: TestCeleryApi,
) -> None:
    task_id = "9c6e9ec1-ffff-450d-a71c-00589415d629"
    get_files_hash_record_repository_mock.init_tasks(
        {
            task_id: Task(
                task_id=task_id,
                hash_type="md5",
                hash_value=None,
                status=PENDING,
                result="",
            )
        }
    )
    get_celery_api_mock.set_task_state(task_id, state=PENDING)
    response = test_app.get("/api/v1/files/compute/hash", params={"task_id": task_id})

    body = response.json()

    assert body == {
        "task_id": "9c6e9ec1-ffff-450d-a71c-00589415d629",
        "hash_type": "md5",
        "hash_value": None,
        "status": "PENDING",
        "result": "",
    }


@pytest.mark.asyncio
async def test_get_already_computed_hash(
    test_app: TestClient,
    get_files_hash_record_repository_mock: TestFilesHashRecordRepository,
    get_celery_api_mock: TestCeleryApi,
) -> None:
    task_id = "9c6e9ec1-ffff-450d-a71c-00589415d629"
    get_files_hash_record_repository_mock.init_tasks(
        {
            task_id: Task(
                task_id=task_id,
                hash_type="md5",
                hash_value="simple hash",
                status=SUCCESS,
                result="",
            )
        }
    )
    response = test_app.get("/api/v1/files/compute/hash", params={"task_id": task_id})

    body = response.json()

    assert body == {
        "task_id": "9c6e9ec1-ffff-450d-a71c-00589415d629",
        "hash_type": "md5",
        "hash_value": "simple hash",
        "status": "SUCCESS",
        "result": "",
    }


@pytest.mark.asyncio
async def test_get_now_computed_hash(
    test_app: TestClient,
    get_files_hash_record_repository_mock: TestFilesHashRecordRepository,
    get_celery_api_mock: TestCeleryApi,
) -> None:
    task_id = "9c6e9ec1-ffff-450d-a71c-00589415d629"
    get_files_hash_record_repository_mock.init_tasks(
        {
            task_id: Task(
                task_id=task_id,
                hash_type="md5",
                hash_value=None,
                status=PENDING,
                result="",
            )
        }
    )
    get_celery_api_mock.set_task_state(
        task_id, state=SUCCESS, result={"hash": "simple hash"}
    )
    response = test_app.get("/api/v1/files/compute/hash", params={"task_id": task_id})

    body = response.json()

    assert body == {
        "task_id": "9c6e9ec1-ffff-450d-a71c-00589415d629",
        "hash_type": "md5",
        "hash_value": "simple hash",
        "status": "SUCCESS",
        "result": "",
    }


@pytest.mark.asyncio
async def test_get_now_failure_computed_hash(
    test_app: TestClient,
    get_files_hash_record_repository_mock: TestFilesHashRecordRepository,
    get_celery_api_mock: TestCeleryApi,
) -> None:
    task_id = "9c6e9ec1-ffff-450d-a71c-00589415d629"
    get_files_hash_record_repository_mock.init_tasks(
        {
            task_id: Task(
                task_id=task_id,
                hash_type="md5",
                hash_value=None,
                status=PENDING,
                result="",
            )
        }
    )
    get_celery_api_mock.set_task_state(task_id, state=FAILURE, result="something wrong")
    response = test_app.get("/api/v1/files/compute/hash", params={"task_id": task_id})

    body = response.json()

    assert body == {
        "task_id": "9c6e9ec1-ffff-450d-a71c-00589415d629",
        "hash_type": "md5",
        "hash_value": None,
        "status": "FAILURE",
        "result": '"something wrong"',
    }
