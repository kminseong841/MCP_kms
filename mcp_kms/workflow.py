# <workflow.py> - Gemini version.
from langgraph.graph import START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.runnables.base import Runnable
import json
import asyncio
from mcp_kms.agent.logging import save_log
from mcp_kms.agent import model
from mcp_kms.agent.mcp_tools import get_langChainTools
from mcp_kms.agent.node_action import CallModelNode
from mcp_kms.agent.graph import build_graph
from mcp_kms.utils.service import McpService


async def agent_test(user_prompt: str) -> json:
    service = McpService()
    session = await service.start_session(server_url="http://0.0.0.0:8000/sse")

    #1) Connect with Structured Tools
    tools = await get_langChainTools(session)
    model_with_tools: Runnable =  model.bind_tools(tools)

    #2) Build Graph
    nodes = {"call_model": CallModelNode(model_with_tools), "tools": ToolNode(tools)}
    edges = {START: "call_model", "tools": "call_model"}
    conditional_edges = {"call_model": tools_condition}

    graph = build_graph(nodes, edges, conditional_edges)
    
    response = await graph.ainvoke({"messages": [("user", user_prompt)]})
    save_log(text=response)

    await service.end_session()
    return response
    

asyncio.run(agent_test(user_prompt="2와5를 더한 결과를 삼각형 pattern으로 출력해줘"))