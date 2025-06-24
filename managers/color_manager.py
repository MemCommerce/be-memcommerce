from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from schemas.colors_schemas import Color, ColorData
from models.color_model import ColorModel


class ColorManager:
    @staticmethod
    async def insert_color(color_data: ColorData, db: AsyncSession) -> Color:
        color = ColorModel(**color_data.model_dump())
        db.add(color)
        await db.commit()
        return Color.model_validate(color)

    @staticmethod
    async def select_all_colors(db: AsyncSession) -> list[Color]:
        colors = (await db.execute(select(ColorModel))).scalars().all()
        return [Color.model_validate(color) for color in colors]

    @staticmethod
    async def delete_color_by_id(id: str, db: AsyncSession) -> None:
        statement = delete(ColorModel).where(ColorModel.id == id)
        await db.execute(statement)
        await db.commit()
