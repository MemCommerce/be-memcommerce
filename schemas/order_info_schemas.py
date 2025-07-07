from pydantic import BaseModel

from schemas.order_items_schemas import OrderItemResponse, OrderItem
from schemas.order_schemas import Order


class OrderInfo(BaseModel):
    order: Order
    order_items: list[OrderItem]


class OrdersInfos(BaseModel):
    orders: list[OrderInfo]


class OrderInfoResponse(BaseModel):
    order: Order
    order_items: list[OrderItemResponse]


class OrdersInfosResponse(BaseModel):
    orders: list[OrderInfoResponse]
