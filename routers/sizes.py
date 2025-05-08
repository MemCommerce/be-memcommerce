from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.size_schemas import Size, SizeData
from managers.size_manager import SizeManager


router = APIRouter(prefix="/sizes")


@router.post("/", response_model=Size, status_code=status.HTTP_201_CREATED)
async def post_size(size_data: SizeData, db: AsyncSession = Depends(get_db)):
    size = await SizeManager.insert_size(size_data, db)
    return size


@router.get("/", response_model=list[Size])
async def get_all_sizes(db: AsyncSession = Depends(get_db)):
    sizes = await SizeManager.select_all_sizes(db)
    return sizes


@router.delete("/{size_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_size(size_id: str, db: AsyncSession = Depends(get_db)):
    await SizeManager.delete_size_by_id(size_id, db)
    return "OK"
