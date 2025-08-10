from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound


from db import get_db
from auth.token import get_current_user_id
from schemas.refund_schemas import RefundCreate, Refund, RefundStatusUpdate
from managers.refund_manager import RefundManager


router = APIRouter(prefix="/refunds", tags=["refunds"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Refund)
async def post_refund(
    data: RefundCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Create a new refund."""
    return await RefundManager.create_refund(data, user_id, db)


@router.get("/", response_model=list[Refund])
async def get_user_refunds(
    user_id: str = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)
):
    return await RefundManager.select_user_refunds(user_id, db)


@router.patch("/{refund_id}", response_model=Refund)
async def patch_refund_status(
    refund_id: str,
    status_update: RefundStatusUpdate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await RefundManager.update_refund_status(
            refund_id, status_update.status, db
        )
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Refund not found")

