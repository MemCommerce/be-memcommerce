from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from auth_providers.google_auth import google_sso
from config import GOOGLE_CALLBACK_URL, FRONT_END_GOOGLE_LOGIN_URL
from schemas.user_schemas import UserCreate
from managers.user_manager import UserManager
from auth.token import create_access_token


router = APIRouter(prefix="/auth")


@router.get("/login", tags=["Google SSO"])
async def google_login():
    return await google_sso.get_login_url(
        redirect_uri=GOOGLE_CALLBACK_URL,
        params={"prompt": "consent", "access_type": "offline"},
    )


@router.get("/callback", tags=["Google SSO"])
async def google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    user = await google_sso.verify_and_process(request)
    if not user:
        return RedirectResponse(
            url=f"{FRONT_END_GOOGLE_LOGIN_URL}?error=Invalid%20user",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    user_stored = await UserManager.select_user_by_email(user.email, db)
    if not user_stored:
        user_to_add = UserCreate(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        user_stored = await UserManager.insert_user(user_to_add, db)
    token = create_access_token(user_stored)
    response = RedirectResponse(
        url=f"{FRONT_END_GOOGLE_LOGIN_URL}?token={token}",
        status_code=status.HTTP_302_FOUND,
    )
    return response
