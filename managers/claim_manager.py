from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from schemas.claim_data_schemas import ClaimDataReq, ClaimDataRes
from schemas.claim_schemas import Claim, ClaimStatusEnum
from schemas.claim_item_schemas import ClaimItem
from models.claim_model import ClaimModel
from models.claim_item_model import ClaimItemModel


class ClaimManager:
    @staticmethod
    async def create_claim(
        data: ClaimDataReq, user_id: str, db: AsyncSession
    ) -> ClaimDataRes:
        claim_row = ClaimModel(**data.claim_request.model_dump(), user_id=user_id)
        db.add(claim_row)
        await db.commit()
        claim_items_rows = [
            ClaimItemModel(**item.model_dump(), claim_id=claim_row.id)
            for item in data.items
        ]
        db.add_all(claim_items_rows)
        await db.commit()

        claim_items = [ClaimItem.model_validate(item) for item in claim_items_rows]
        claim = Claim.model_validate(claim_row)

        return ClaimDataRes(claim_request=claim, items=claim_items)

    @staticmethod
    async def select_user_claims(user_id: str, db: AsyncSession) -> list[ClaimDataRes]:
        result = await db.execute(
            select(ClaimModel)
                .where(ClaimModel.user_id == user_id)
                .options(selectinload(ClaimModel.items))
        )
        claim_rows = result.scalars().all()

        return [
            ClaimDataRes(
                claim_request=Claim.model_validate(claim_row),
                items=[ClaimItem.model_validate(item) for item in claim_row.items],
            )
            for claim_row in claim_rows
        ]

    @staticmethod
    async def update_claim_status(
        claim_id: str, status: ClaimStatusEnum, db: AsyncSession
    ) -> Claim:
        result = await db.execute(select(ClaimModel).where(ClaimModel.id == claim_id))
        claim = result.scalars().first()

        if not claim:
            raise ValueError("Claim not found")

        claim.status = status  # type: ignore[reportAttributeAccessIssue]
        await db.commit()
        await db.refresh(claim)

        return Claim.model_validate(claim)
