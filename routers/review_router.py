from fastapi import APIRouter, status, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from httpx import AsyncClient

from db import get_db
from auth.token import get_current_user_id
from schemas.review_schemas import Review, ReviewData, ReviewSentiment
from managers.review_manager import ReviewManager
from config import REVIEW_PROCESS_START_URL


router = APIRouter(prefix="/reviews", tags=["Reviews"])


async def post_review_process(review: Review):
    async with AsyncClient() as client:
        body = review.model_dump()
        await client.post(REVIEW_PROCESS_START_URL, json=body, timeout=300)


@router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
async def post_review(
    data: ReviewData,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    review = await ReviewManager.insert_review(data, db, user_id)
    background_tasks.add_task(post_review_process, review)
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


@router.patch("/{review_id}/sentiment", response_model=Review)
async def patch_review_sentiment(review_id: str, data: ReviewSentiment, db: AsyncSession = Depends(get_db)):
    updated_review = await ReviewManager.update_review_sentiment(review_id, data, db)
    return updated_review


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
