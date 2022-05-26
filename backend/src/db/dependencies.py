from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.respositories.files_hash_record import FilesHashRecordRepository


# Dependency
async def get_session(request: Request) -> AsyncSession:
    async_session = request.app.state.db

    async with async_session() as session:
        yield session


async def get_files_hash_record_repository(
    session: AsyncSession = Depends(get_session),
) -> FilesHashRecordRepository:
    return FilesHashRecordRepository(session)
