from os import environ
from dotenv import load_dotenv

load_dotenv()

JWT_KEY = environ["JWT_KEY"]

DB_USER = environ["DB_USER"]
DB_PASSWORD = environ["DB_PASSWORD"]
DB_HOST = environ["DB_HOST"]
DB_NAME = environ["DB_NAME"]
TEST_DB_NAME = environ.get("TEST_DB_NAME")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{TEST_DB_NAME}"
)


GOOGLE_CLIENT_ID = environ["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = environ["GOOGLE_CLIENT_SECRET"]

FRONT_END_GOOGLE_LOGIN_URL = environ.get("FRONT_END_GOOGLE_LOGIN_URL")
