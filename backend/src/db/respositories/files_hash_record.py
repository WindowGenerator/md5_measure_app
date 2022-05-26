from typing import Optional

from celery.states import PENDING
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import Base
from src.db.models import FilesHashRecord
from src.schemas.files import Task


def _alchemy_model2dict(model: Base):
    out_dict = {}
    for column in model.__table__.columns:
        out_dict[column.name] = getattr(model, column.name)

    return out_dict


class FilesHashRecordRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_hash_record(self, task_id: str) -> Task:
        result = await self._session.execute(
            select(FilesHashRecord).where(FilesHashRecord.task_id == task_id)
        )
        # FIXME(разобраться): await session.execute запускает неявную транзакцию????
        await self._session.commit()
        task = result.scalar()

        if task is None:
            return None

        return Task(**_alchemy_model2dict(task))

    async def create_hash_record(
        self,
        task_id: str,
        hash_type: str,
        status: str = PENDING,
        result: str = "",
        hash_value: Optional[str] = None,
    ) -> Task:
        query = insert(FilesHashRecord).values(
            task_id=task_id,
            hash_value=hash_value,
            hash_type=hash_type,
            status=status,
            result=result,
        )

        async with self._session.begin():
            await self._session.execute(query)

        return await self.get_hash_record(task_id)

    async def update_hash_record(
        self,
        task_id: str,
        status: str = PENDING,
        result: str = "",
        hash_value: Optional[str] = None,
    ) -> Task:
        query = (
            update(FilesHashRecord)
            .where(FilesHashRecord.task_id == task_id)
            .values(status=status, result=result, hash_value=hash_value)
        )

        async with self._session.begin():
            await self._session.execute(query)

        return await self.get_hash_record(task_id)
