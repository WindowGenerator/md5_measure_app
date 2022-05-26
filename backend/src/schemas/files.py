from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel


class TaskPromise(BaseModel):
    task_id: Union[str, UUID]


class Task(TaskPromise):
    hash_type: str
    hash_value: Optional[str]
    status: str
    result: str
