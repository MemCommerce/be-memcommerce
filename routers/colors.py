from fastapi import APIRouter

from schemas.colors_schemas import ColorBase

colors_router = APIRouter(prefix="/colors")


@colors_router.post("/")
async def post_color(color_data: ColorBase):
    print(color_data)
    return "OK"
