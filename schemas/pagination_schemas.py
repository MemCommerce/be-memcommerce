from typing import TypeVar, Generic, List

from pydantic import BaseModel

T = TypeVar("T")


class PaginationResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
