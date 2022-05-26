from fastapi import APIRouter
from src.handlers import files


router = APIRouter()
router.include_router(files.router, tags=["files"])
