from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

from schemas.messages_schemas import Message


class MCPClient:
    def __init__(self) -> None:
         # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai_client = OpenAI()

    async def process_messages(self, messages: list[Message]) -> Message:
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1000,
            messages=messages,
            # tools=available_tools,
        )
        choice_message = response.choices[0].message
        message = Message(role=choice_message.role, content=str(choice_message.content))
        return message
