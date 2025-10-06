# agent.py
# pip install langgraph langchain langchain-mcp-adapters langchain-openai

import asyncio
import os
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv

load_dotenv()

async def main():
    # 1) MCP 서버 연결 설정
    #    FastMCP HTTP 권장 경로: http://localhost:8000/mcp  (끝에 / 유무는 서버 설정에 따라 모두 허용됨)
    client = MultiServerMCPClient(
        {
            "my_server": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )

    # 2) MCP에서 툴 로드 → LangGraph/LC 호환 툴 목록
    tools = await client.get_tools()

    # 3) 모델 + 에이전트 생성 (ReAct 스타일)
    ai_api_key = os.getenv("OPENAI_API_KEY")
    if ai_api_key is None:
        raise RuntimeError("환경변수 OPENAI_API_KEY가 설정되지 않았습니다.")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=ai_api_key)
    agent = create_react_agent(llm, tools)

    # 4) 실행
    user_prompt = "5와 7을 더한 결과로 삼각형 패턴을 그려줘"
    result = await agent.ainvoke({"messages": [{"role": "user", "content": user_prompt}]})
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
