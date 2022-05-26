import json

from celery.result import AsyncResult
from celery.states import READY_STATES, SUCCESS
from fastapi import APIRouter, Depends, UploadFile, status
from src.db.dependencies import get_files_hash_record_repository
from src.db.respositories.files_hash_record import FilesHashRecordRepository
from src.schemas.files import Task, TaskPromise
from src.worker.celery_api import CeleryApi
from src.worker.dependencies import get_celery_api


router = APIRouter(prefix="/files")


@router.post(
    "/compute/hash", response_model=TaskPromise, status_code=status.HTTP_201_CREATED
)
async def compute_hash(
    file: UploadFile,
    hash_type: str = "md5",
    celery_api: CeleryApi = Depends(get_celery_api),
    files_hash_record_repository: FilesHashRecordRepository = Depends(
        get_files_hash_record_repository
    ),
) -> TaskPromise:
    # тут думал посылать не текст файла, а name на tmp файл (так как реализация скарлета tmp файл создает)
    # ну и соответственно расшарить некоторую область файловой системы для хранения этих файлов. Но потом понял,
    # что бэк и воркеры могут быть не на одной физической машине, ну и файловую систему таким образом зафрижу

    # Также думал посылать сжатое содержимое файла, чтобы не так сильно сетевку насиловать при передачи через рэббит
    content = await file.read()
    task = celery_api.compute_hash_by_file(content.decode("utf-8"), hash_type)

    await files_hash_record_repository.create_hash_record(task.id, hash_type)

    return TaskPromise(task_id=task.id)


@router.get("/compute/hash", response_model=Task, status_code=status.HTTP_200_OK)
async def get_computed_hash(
    task_id: str,
    files_hash_record_repository: FilesHashRecordRepository = Depends(
        get_files_hash_record_repository
    ),
) -> Task:
    task_from_db = await files_hash_record_repository.get_hash_record(task_id)

    if task_from_db.status in READY_STATES:
        return task_from_db

    task_from_redis = AsyncResult(task_id)

    if task_from_redis.state not in READY_STATES:
        return task_from_db

    if task_from_redis.state == SUCCESS:
        return await files_hash_record_repository.update_hash_record(
            task_id,
            status=task_from_redis.state,
            hash_value=task_from_redis.result["hash"],
        )
    else:
        return await files_hash_record_repository.update_hash_record(
            task_id,
            status=task_from_redis.state,
            result=json.dump(task_from_redis.result),
        )
