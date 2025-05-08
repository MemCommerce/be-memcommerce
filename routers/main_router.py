from fastapi import APIRouter

from routers import categories, colors, products, sizes


main_router = APIRouter()
main_router.include_router(categories.categories_router)
main_router.include_router(products.products_router)
main_router.include_router(colors.colors_router)
main_router.include_router(sizes.router)
