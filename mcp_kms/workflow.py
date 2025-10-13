# <workflow.py> - Gemini version.
from langgraph.graph import START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.runnables.base import Runnable
import json
import asyncio
from mcp_kms.agent.logging import save_log
from mcp_kms.agent import model
from mcp_kms.agent.mcp_tools import add_tools
from mcp_kms.agent.node_action import CallModelNode
from mcp_kms.agent.graph import build_graph


async def agent_test(user_prompt: str) -> json:
    tools = await add_tools(server_url="http://0.0.0.0:8000/sse")
    model_with_tools: Runnable =  model.bind_tools(tools)

    nodes = {"call_model": CallModelNode(model_with_tools), "tools": ToolNode(tools)}
    edges = {START: "call_model", "tools": "call_model"}
    conditional_edges = {"call_model": tools_condition}

    graph = build_graph(nodes, edges, conditional_edges)
    
    response = await graph.ainvoke({"messages": [("user", user_prompt)]})
    save_log(text=response)
    return response
    

asyncio.run(agent_test(user_prompt="2와5를 더한 결과를 삼각형 pattern으로 출력해줘"))