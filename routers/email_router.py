from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.email_schemas import EmailDetails
from message_services.gmail_service import send_message
from managers.user_manager import UserManager


router = APIRouter(prefix="/emails", tags=["Email"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_email_to_user(data: EmailDetails, db: AsyncSession = Depends(get_db)):
    user = await UserManager.select_user_by_id(data.user_id, db)
    send_message(user.email, data.subject, data.content)
    return "OK"
