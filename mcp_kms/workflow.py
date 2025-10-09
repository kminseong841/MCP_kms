# <workflow.py> - Gemini 버전
from mcp import ClientSession
from mcp.client.sse import sse_client
from langchain_mcp_adapters.tools import load_mcp_tools
# [변경] OpenAI 대신 Google Generative AI 라이브러리를 임포트합니다.
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
import config
import json
import asyncio
import pprint

def save_log(text: dict):
    with open(file="result.txt", mode="w") as f:
        printer = pprint.PrettyPrinter(stream=f, indent=4)
        printer.pprint(text)
# [변경] 언어 모델을 ChatGoogleGenerativeAI로 설정합니다.
# config.py 파일에 google_api_key를 추가해야 합니다.
# 예: model = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", google_api_key=config.google_api_key)
model = ChatGoogleGenerativeAI(model=config.model, google_api_key=config.google_api_key)


async def agent_test(user_prompt: str) -> json:
    # 세션 설정
    async with sse_client(url="http://0.0.0.0:8000/sse") as (reader, writer):
        async with ClientSession(read_stream=reader, write_stream=writer) as session:
            await session.initialize()
            tools = await load_mcp_tools(session=session)

            # 툴 리스트
            def call_model(state: MessagesState):
                # model.bind_tools(tools) 부분은 LangChain의 표준 인터페이스이므로 변경할 필요가 없습니다.
                response = model.bind_tools(tools).invoke(state["messages"])
                return {"messages": [response]}
            
            # LangGraph 구성은 기존과 동일합니다.
            builder = StateGraph(MessagesState)
            builder.add_node("call_model", call_model) # call_model 노드의 이름을 명시적으로 지정
            builder.add_node("tools", ToolNode(tools)) # tools 노드의 이름 명시
            builder.add_edge(START, "call_model")
            builder.add_conditional_edges(
                "call_model",
                tools_condition
            )
            builder.add_edge("tools", "call_model")
            graph = builder.compile()
            
            # LangGraph 실행부의 입력 형식에 맞게 수정합니다.
            # MessagesState는 "messages" 키에 메시지 리스트를 받습니다.
            response = await graph.ainvoke({"messages": [("user", user_prompt)]})
            save_log(text=response)
            pprint.pprint(response)
            return response
    

# 참고: LangGraph의 MessagesState는 HumanMessage, AIMessage 등 메시지 객체 리스트를 기대합니다.
# 간단한 테스트를 위해 문자열을 튜플 형태로 전달합니다.
asyncio.run(agent_test(user_prompt="2와5를 더한 결과를 삼각형 pattern으로 출력해줘"))