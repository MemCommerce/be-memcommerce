from pydantic import BaseModel


class EmailDetails(BaseModel):
    user_id: str
    subject: str
    content: str
