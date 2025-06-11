from fastapi import APIRouter, status

from schemas.messages_schemas import Message
from mcp_clients.openai_client import MCPClient

router = APIRouter(prefix="/ai-admin")


@router.post("/", response_model=Message, status_code=status.HTTP_201_CREATED)
async def post_messages(messages: list[Message]):
    client = MCPClient()
    ai_message = await client.process_messages(messages)
    return ai_message
