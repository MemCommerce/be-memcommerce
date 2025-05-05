from fastapi import APIRouter

from routers import category_router, products_router


main_router = APIRouter()
main_router.include_router(category_router.category_router)
main_router.include_router(products_router.products_router)
