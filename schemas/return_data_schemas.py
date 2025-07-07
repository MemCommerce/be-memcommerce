from pydantic import BaseModel

from schemas.return_schemas import ReturnCreate, Return
from schemas.return_item_schemas import ReturnItemCreate, ReturnItem


class ReturnDataReq(BaseModel):
    return_request: ReturnCreate
    items: list[ReturnItemCreate]


class ReturnDataRes(BaseModel):
    return_request: Return
    items: list[ReturnItem]
