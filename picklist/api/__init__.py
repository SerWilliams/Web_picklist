from fastapi import APIRouter

from .converter import router as converter_router

router = APIRouter()
router.include_router(converter_router)