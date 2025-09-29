from mcp import ClientSession
from mcp.client.sse import sse_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from config import config
import json
import asyncio

# 언어 모델 설정
model = ChatOpenAI(model=config.model, api_key="empty", base_url=config.api_url)


async def agent_test(user_prompt: str) -> json:
    # 세션 설정
    async with sse_client(url="http://localhost:8000/sse") as (reader, writer):
        async with ClientSession(read_stream=reader, write_stream=writer) as session:
            await session.initialize()
            tools = await load_mcp_tools(session=session)

            # 툴 리스트
            def call_model(state: MessagesState):
                response = model.bind_tools(tools).invoke(state["message"])
                return {"messages": response}
            
            builder = StateGraph(MessagesState)
            builder.add_node(call_model)
            builder.add_node(ToolNode(tools))
            builder.add_edge(START, "call_model")
            builder.add_conditional_edges(
                "call_model",
                tools_condition
            )
            builder.add_edge("tools", "call_model")
            graph = builder.compile()
            response = await graph.ainvoke({"messages": user_prompt})
            return response
        

asyncio.run(agent_test(user_prompt="What is the today's weather?"))