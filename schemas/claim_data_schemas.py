from pydantic import BaseModel

from schemas.claim_schemas import ClaimCreate, Claim
from schemas.claim_item_schemas import ClaimItemCreate, ClaimItem


class ClaimDataReq(BaseModel):
    claim_request: ClaimCreate
    items: list[ClaimItemCreate]


class ClaimDataRes(BaseModel):
    claim_request: Claim
    items: list[ClaimItem]
