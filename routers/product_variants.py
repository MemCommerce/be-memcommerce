from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.product_variant_schemas import (
    ProductVariantResp,
    ProductVariantData,
    ProductVariantCreate,
)
from managers.product_variant_manager import ProductVariantManager
from utils.image_compression import compress_image_to_webp
from utils.utils import separate_data_url_from_base64
from storage.gcp_storage import upload_bytes_image, generate_signed_url

router = APIRouter(prefix="/product-variants")


@router.post(
    "/", response_model=ProductVariantResp, status_code=status.HTTP_201_CREATED
)
async def post_product_variant(
    product_variant_req: ProductVariantCreate, db: AsyncSession = Depends(get_db)
):
    if product_variant_req.image:
        image_bytes = compress_image_to_webp(
            separate_data_url_from_base64(product_variant_req.image)[1]
        )
        img_file_name_str = upload_bytes_image(image_bytes)
    else:
        img_file_name_str = None
    product_variabt_data = ProductVariantData(
        price=product_variant_req.price,
        color_id=product_variant_req.color_id,
        size_id=product_variant_req.size_id,
        product_id=product_variant_req.product_id,
    )
    product_variant = await ProductVariantManager.insert_product_variant(
        product_variabt_data, img_file_name_str, db
    )
    signed_url = generate_signed_url(product_variant.image_name)
    response = ProductVariantResp.from_product_variant(product_variant, signed_url)
    return response


@router.get("/", response_model=list[ProductVariantResp])
async def get_all_pv(db: AsyncSession = Depends(get_db)):
    product_variants = await ProductVariantManager.select_all_pv(db)
    # TODO optimize generation of signed urls
    pvrs = [
        ProductVariantResp.from_product_variant(
            pv, generate_signed_url(pv.image_name) if pv.image_name else ""
        )
        for pv in product_variants
    ]
    return pvrs


@router.delete("/{product_variant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pv(product_variant_id: str, db: AsyncSession = Depends(get_db)):
    await ProductVariantManager.delete_product_variant(product_variant_id, db)
    return "OK"
