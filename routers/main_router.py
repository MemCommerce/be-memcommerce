from fastapi import APIRouter

from routers import categories, colors, products, sizes, product_variants, storefront_router


main_router = APIRouter()
main_router.include_router(categories.categories_router)
main_router.include_router(products.products_router)
main_router.include_router(colors.colors_router)
main_router.include_router(sizes.router)
main_router.include_router(product_variants.router)
main_router.include_router(storefront_router.router)
