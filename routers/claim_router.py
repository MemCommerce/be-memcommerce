from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession


from db import get_db
from auth.token import get_current_user_id
from schemas.claim_data_schemas import ClaimDataReq, ClaimDataRes
from schemas.claim_schemas import Claim, ClaimStatusUpdate
from managers.claim_manager import ClaimManager


router = APIRouter(prefix="/claims", tags=["claims"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ClaimDataRes)
async def post_claim(
    data: ClaimDataReq,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Create a new claim."""
    return await ClaimManager.create_claim(data, user_id, db)


@router.get("/", response_model=list[ClaimDataRes])
async def get_user_claims(
    user_id: str = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)
):
    return await ClaimManager.select_user_claims(user_id, db)


@router.patch("/{claim_id}", response_model=Claim)
async def patch_claim_status(
    claim_id: str,
    status_update: ClaimStatusUpdate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await ClaimManager.update_claim_status(claim_id, status_update.status, db)

