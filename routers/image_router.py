from fastapi import APIRouter, status

from schemas.image_schemas import TempImage, TempImageCreate
from utils.image_compression import compress_image_to_webp
from utils.utils import separate_data_url_from_base64
from storage.gcp_storage import upload_bytes_image, generate_signed_url


router = APIRouter(prefix="/images", tags=["Images"])


@router.post("/temporary", response_model=TempImage, status_code=status.HTTP_201_CREATED)
async def post_temporary_image(image_data: TempImageCreate):
    image_bytes = compress_image_to_webp(separate_data_url_from_base64(image_data.base64_data)[1])
    image_file_name_str = upload_bytes_image(image_bytes)
    signer_url = generate_signed_url(image_file_name_str)
    temp_image = TempImage(name=image_file_name_str, url=signer_url)
    return temp_image


@router.post("/temporary/bulk", response_model=list[TempImage], status_code=status.HTTP_201_CREATED)
async def post_bulk_temporary_images(images_datas: list[TempImageCreate]):
    temp_images = []
    for image_data in images_datas:
        image_bytes = compress_image_to_webp(separate_data_url_from_base64(image_data.base64_data)[1])
        image_file_name_str = upload_bytes_image(image_bytes)
        signer_url = generate_signed_url(image_file_name_str)
        temp_image = TempImage(name=image_file_name_str, url=signer_url)
        temp_images.append(temp_image)
    return temp_images
