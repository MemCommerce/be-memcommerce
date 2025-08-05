from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from db import get_db
from schemas.review_schemas import Review, ReviewData
from managers.review_manager import ReviewManager


router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
async def post_review(data: ReviewData, db: AsyncSession = Depends(get_db)):
    review = await ReviewManager.insert_review(data, db)
    return review


@router.get("/{review_id}", response_model=Review)
async def get_by_id(review_id: str, db: AsyncSession = Depends(get_db)):
    try:
        review = await ReviewManager.select_review_by_id(review_id, db)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No review found with id {review_id}",
        )

    return review


@router.put("/{review_id}", response_model=Review)
async def put_review(
    review_id: str, data: ReviewData, db: AsyncSession = Depends(get_db)
):
    try:
        review = await ReviewManager.update_review(review_id, data, db)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No review found with id {review_id}",
        )

    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(review_id: str, db: AsyncSession = Depends(get_db)):
    try:
        await ReviewManager.delete_review(review_id, db)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No review found with id {review_id}",
        )

    return "OK"
