from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from auth.token import get_current_user_id
from schemas.return_data_schemas import ReturnDataReq, ReturnDataRes
from managers.return_manager import ReturnManager


router = APIRouter(prefix="/returns", tags=["returns"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReturnDataRes)
async def post_return(
    data: ReturnDataReq,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new return request.
    """
    return_data = await ReturnManager.create_return(data, user_id, db)

    return return_data


@router.get("/", response_model=list[ReturnDataRes])
async def get_user_returns(
    user_id: str = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)
):
    returns_datas = await ReturnManager.select_user_returns(user_id, db)
    return returns_datas
