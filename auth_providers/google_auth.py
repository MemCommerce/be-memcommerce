from fastapi_sso.sso.google import GoogleSSO

from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_CALLBACK_URL, IS_DEV


google_sso = GoogleSSO(
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_CALLBACK_URL,
    allow_insecure_http=IS_DEV,
)
