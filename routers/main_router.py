from fastapi import APIRouter

from routers import category_router


main_router = APIRouter()
main_router.include_router(category_router.category_router)
