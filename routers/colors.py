from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

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


@colors_router.put("/{color_id}", response_model=Color)
async def put_category(
    color_id: str, color_data: ColorData, db: AsyncSession = Depends(get_db)
):
    try:
        updated_category = await ColorManager.update_color(color_id, color_data, db)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No color found with id {color_id}.",
        )

    return updated_category
