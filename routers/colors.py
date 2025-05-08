from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.colors_schemas import ColorData, Color
from managers.color_manager import ColorManager
from db import get_db

colors_router = APIRouter(prefix="/colors")


@colors_router.post("/", response_model=Color, status_code=status.HTTP_201_CREATED)
async def post_color(color_data: ColorData, db: AsyncSession = Depends(get_db)):
    color = await ColorManager.insert_color(color_data, db)
    return color


@colors_router.get("/", response_model=list[Color])
async def get_all_colors(db: AsyncSession = Depends(get_db)):
    colors = await ColorManager.select_all_colors(db)
    return colors


@colors_router.delete("/{color_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_color(color_id: str, db: AsyncSession = Depends(get_db)):
    await ColorManager.delete_color_by_id(color_id, db)
    return "OK"
