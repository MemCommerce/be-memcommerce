from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from models.review_model import ReviewModel
from models.order_item_model import OrderItemModel
from models.order_model import OrderModel
from schemas.review_schemas import Review, ReviewData, ReviewSentiment
from schemas.order_items_schemas import OrderItem


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
    async def update_review_sentiment(review_id: str, sentiment_data: ReviewSentiment, db: AsyncSession) -> Review:
        stmt = select(ReviewModel).where(ReviewModel.id == review_id)
        result = await db.execute(stmt)
        review = result.scalar_one_or_none()

        if not review:
            raise NoResultFound()
        
        for field, value in sentiment_data.model_dump(exclude_unset=True).items():
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

    @staticmethod
    async def select_reviews_with_order_items_by_user_id(
        user_id: str, db: AsyncSession
    ) -> list[tuple[Optional[Review], OrderItem]]:
        """Return all order items for a user with their related reviews if any."""
        stmt = (
            select(ReviewModel, OrderItemModel)
            .select_from(OrderItemModel)
            .join(OrderModel, OrderItemModel.order_id == OrderModel.id)
            .outerjoin(ReviewModel, ReviewModel.order_item_id == OrderItemModel.id)
            .where(OrderModel.user_id == user_id)
        )
        result = await db.execute(stmt)
        rows = result.all()

        return [
            (
                Review.model_validate(review_row) if review_row else None,
                OrderItem.model_validate(order_item_row),
            )
            for review_row, order_item_row in rows
        ]
