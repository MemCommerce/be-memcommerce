# be-memcommerce

Backend service for the memcommerce project built with FastAPI and PostgreSQL.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

## Setup

1. **Install uv** if it's not already installed:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. **Install dependencies**:
   ```bash
   uv sync
   ```
3. **Create a `.env` file** or export the environment variables listed below.

## Environment variables

| Variable | Description |
|----------|-------------|
| `JWT_KEY` | Secret key for signing JWT tokens |
| `DB_USER` | PostgreSQL user |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | PostgreSQL host |
| `DB_NAME` | PostgreSQL database name |
| `TEST_DB_NAME` | (optional) database name used for tests |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret |
| `GOOGLE_CALLBACK_URL` | (optional) OAuth callback URL, defaults to `http://localhost:8001/auth/callback` |
| `IS_DEV` | (optional) flag to enable development specific behaviour |
| `SA_KEY_PATH` | (optional) path to a Google service account key file |
| `SA_CREDENTIALS` | (optional) JSON string of service account credentials, used instead of `SA_KEY_PATH` |
| `BUCKET_NAME` | Google Cloud Storage bucket for uploaded assets |
| `GMAIL_ADDRESS` | Gmail address used for outgoing mail |
| `GMAIL_APP_PASSWORD` | Application password for the Gmail account |
| `REVIEW_PROCESS_START_URL` | URL that triggers the review process |

## Running the server

Use uv to run the FastAPI application:

```bash
uv run fastapi dev main.py
```

Alternatively, you can run with uvicorn directly:

```bash
uv run uvicorn main:app --reload
```

## Project structure

```
.
├── auth/              # Authentication logic and security utilities
├── auth_providers/    # Integrations with external auth providers (e.g. Google)
├── managers/          # Higher level business logic
├── message_services/  # Email and messaging helpers
├── models/            # SQLAlchemy ORM models
├── routers/           # API route definitions
├── schemas/           # Pydantic models for request/response bodies
├── storage/           # Google Cloud Storage helpers
├── utils/             # Miscellaneous utilities
├── migrations/        # Database migration SQL scripts
└── main.py            # FastAPI application entry point
```

This structure separates concerns between routing, business logic, persistence, and external service integrations, providing a clear foundation for further development.

