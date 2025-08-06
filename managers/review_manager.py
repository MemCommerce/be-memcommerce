from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from models.review_model import ReviewModel
from schemas.review_schemas import Review, ReviewData


class ReviewManager:
    @staticmethod
    async def insert_review(data: ReviewData, db: AsyncSession, user_id: str) -> Review:
        review = ReviewModel(**data.model_dump(), user_id=user_id)
        db.add(review)
        await db.commit()
        return Review.model_validate(review)
    
    @staticmethod
    async def select_review_by_id(review_id: str, db: AsyncSession) -> Review:
        stmt = select(ReviewModel).where(ReviewModel.id == review_id)
        review = (await db.execute(stmt)).scalar_one_or_none()

        if not review:
            raise NoResultFound()
        
        return Review.model_validate(review)
    
    @staticmethod
    async def select_review_by_order_item_id(order_item_id: str, db: AsyncSession) -> Optional[Review]:
        stmt = select(ReviewModel).where(ReviewModel.order_item_id == order_item_id)
        review = (await db.execute(stmt)).scalar_one_or_none()

        if not review:
            return None
        
        return Review.model_validate(review)
    
    @staticmethod
    async def update_review(review_id: str, data: ReviewData, db: AsyncSession) -> Review:
        stmt = select(ReviewModel).where(ReviewModel.id == review_id)
        result = await db.execute(stmt)
        review = result.scalar_one_or_none()

        if not review:
            raise NoResultFound()

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(review, field, value)

        await db.commit()
        await db.refresh(review)

        return Review.model_validate(review)
    
    @staticmethod
    async def delete_review(review_id: str, db: AsyncSession) -> None:
        stmt = select(ReviewModel).where(ReviewModel.id == review_id)
        result = await db.execute(stmt)
        review = result.scalar_one_or_none()

        if not review:
            raise NoResultFound()

        await db.delete(review)
        await db.commit()
