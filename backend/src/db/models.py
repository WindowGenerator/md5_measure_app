from uuid import uuid4

from celery.states import PENDING
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from src.db.database import Base


class FilesHashRecord(Base):
    __tablename__ = "files_hash_record"

    task_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    hash_value = Column(String, nullable=True)
    hash_type = Column(String, nullable=False)
    status = Column(String, nullable=False, default=PENDING)
    result = Column(String, nullable=False, default="")
