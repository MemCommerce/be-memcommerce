from typing import Optional
from contextlib import AsyncExitStack, asynccontextmanager
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import Tool
from openai import OpenAI
from openai.types.responses import ResponseFunctionToolCall

from schemas.messages_schemas import Message


class MCPClient:
    def __init__(self) -> None:
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai_client = OpenAI()

    @asynccontextmanager
    async def get_session(self):
        async with streamablehttp_client("http://localhost:8000/mcp/") as transport:
            async with ClientSession(transport[0], transport[1]) as session:
                await session.initialize()
                yield session
                
    async def list_tools(self) -> list[Tool]:
        async with self.get_session() as session:
            response = await session.list_tools()
            tools = response.tools
            print("Available tools:", [tool.name for tool in tools])
            return tools
        
    async def call_tool(self, tool_name, **kwargs):
        async with self.get_session() as session:
            result = await session.call_tool(tool_name, kwargs)
            print(result)
            return result

    async def connect_to_mcp_server(self) -> None:
        async with streamablehttp_client("http://localhost:8000/mcp/") as transport:
            async with ClientSession(transport[0], transport[1]) as session:
                await session.initialize()
                response = await session.list_tools()
                tools = response.tools
                print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_messages_two(self, messages: list[Message]) -> list[Message]:
        available_tools = await self.list_tools()
        tools = [{
            "type": "function",
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.inputSchema
        } for tool in available_tools]

        response = self.openai_client.responses.create(
            model="gpt-4.1",
            input=messages,
            tools=tools
        )

        new_messages: list[Message] = []
        for item in response.output:
            if isinstance(item, ResponseFunctionToolCall):
                arguments = json.loads(item.arguments)
                tool_call_result = await self.call_tool(item.name, **arguments)
                new_input = messages + [item, {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": str(tool_call_result.content)
                }]
                final_response = self.openai_client.responses.create(
                    model="gpt-4.1",
                    input=new_input,
                    tools=tools
                )
                new_messages.append(Message(role="assistant", content=final_response.output_text))

            else:
                content = item.content[0]
                new_messages.append(Message(role="assistant", content=content.text))

        return new_messages
    
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()
