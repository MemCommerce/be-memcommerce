from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from schemas.return_data_schemas import ReturnDataReq, ReturnDataRes
from schemas.return_schemas import Return
from schemas.return_item_schemas import ReturnItem
from models.return_model import ReturnModel
from models.return_item_model import ReturnItemModel


class ReturnManager:
    @staticmethod
    async def create_return(
        data: ReturnDataReq, user_id: str, db: AsyncSession
    ) -> ReturnDataRes:
        return_request_rows = ReturnModel(
            **data.return_request.model_dump(), user_id=user_id
        )
        db.add(return_request_rows)
        await db.commit()
        return_items_rows = [
            ReturnItemModel(**item.model_dump(), return_id=return_request_rows.id)
            for item in data.items
        ]
        db.add_all(return_items_rows)
        await db.commit()

        return_items = [ReturnItem.model_validate(item) for item in return_items_rows]
        return_request = Return.model_validate(return_request_rows)

        return ReturnDataRes(return_request=return_request, items=return_items)

    @staticmethod
    async def select_user_returns(user_id: str, db: AsyncSession) -> list[ReturnDataRes]:
        result = await db.execute(
            select(ReturnModel)
            .where(ReturnModel.user_id == user_id)
            .options(selectinload(ReturnModel.items))
        )
        return_rows = result.scalars().all()

        return [
            ReturnDataRes(
                return_request=Return.model_validate(return_row),
                items=[ReturnItem.model_validate(item) for item in return_row.items],
            )
            for return_row in return_rows
        ]