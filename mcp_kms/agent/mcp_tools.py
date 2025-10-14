from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.tools.base import BaseTool
from mcp import ClientSession


async def get_langChainTools(session: ClientSession) -> list[BaseTool]:
    tools = await load_mcp_tools(session=session)
    return tools