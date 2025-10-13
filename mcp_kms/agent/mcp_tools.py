from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.tools.base import BaseTool
from mcp.client.sse import sse_client
from mcp import ClientSession


async def add_tools(server_url:str) -> list[BaseTool]:
    async with sse_client(url=server_url) as (reader, writer):
        async with ClientSession(read_stream=reader, write_stream=writer) as session:
            await session.initialize()
            tools = await load_mcp_tools(session=session)
            return tools