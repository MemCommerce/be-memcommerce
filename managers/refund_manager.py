from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from schemas.refund_schemas import (
    RefundCreate,
    Refund,
    RefundStatusEnum,
)
from models.refund_model import RefundModel


class RefundManager:
    @staticmethod
    async def create_refund(
        data: RefundCreate, user_id: str, db: AsyncSession
    ) -> Refund:
        refund_row = RefundModel(**data.model_dump(), user_id=user_id)
        db.add(refund_row)
        await db.commit()
        await db.refresh(refund_row)

        return Refund.model_validate(refund_row)

    @staticmethod
    async def select_user_refunds(user_id: str, db: AsyncSession) -> list[Refund]:
        result = await db.execute(
            select(RefundModel).where(RefundModel.user_id == user_id)
        )
        refund_rows = result.scalars().all()

        return [Refund.model_validate(row) for row in refund_rows]

    @staticmethod
    async def update_refund_status(
        refund_id: str, status: RefundStatusEnum, db: AsyncSession
    ) -> Refund:
        result = await db.execute(select(RefundModel).where(RefundModel.id == refund_id))
        refund = result.scalars().first()

        if not refund:
            raise NoResultFound

        refund.status = status  # type: ignore[reportAttributeAccessIssue]
        await db.commit()
        await db.refresh(refund)

        return Refund.model_validate(refund)
