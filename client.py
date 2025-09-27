# client.py
import asyncio
from fastmcp import Client

# 서버가 HTTP로 떠 있다고 가정 (위 server.py와 동일 포트)
client = Client("http://localhost:8000/mcp")

async def main():
    async with client:
        # 서버에 등록된 MCP Tool 호출
        result = await client.call_tool("add", {"a": 5, "b": 7})
        print("5 + 7 =", result)

if __name__ == "__main__":
    asyncio.run(main())
