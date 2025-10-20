# server.py
from fastmcp import FastMCP
from fastmcp.server.http import create_sse_app
from typing import Callable
import uvicorn

API_KEY = "kms-secret-key"

mcp = FastMCP("My MCP Server")

def bearer_auth_middleware(app) -> Callable:
    async def middleware(scope, receive, send):
        if scope["type"] == "http":
            raw_headers = dict((k.decode().lower(), v.decode()) for k, v in scope.get("headers", []))
            received_key = raw_headers.get("authorization")
            if received_key != f"Bearer {API_KEY}":
                await send({
                    "type": "http.response.start",
                    "status": 401,
                    "headers": [
                        (b"content-type", b"application/json; charset=utf-8"),
                    ],
                })
                await send({
                    "type": "http.response.body",
                    "body": b'{"detail":"Invalid or missing API key"}',
                    "more_body": False,
                })
                return 
            await app(scope, receive, send)

    return middleware


# 데코레이터로 MCP 툴 등록
@mcp.tool
def add(a: int, b: int) -> int:
    """두 정수를 더해 반환합니다."""
    return a + b

@mcp.tool
def print_triangle_pattern(n: int) -> str:
    """삼각형 패턴 문자열을 반환합니다."""
    lines = []
    for i in range(1, n + 1):
        lines.append("*" * i)
    return "\n".join(lines)

if __name__ == "__main__":
    # mcp.run(transport="sse", host="0.0.0.0", port=8000)
    uvicorn.run(app=bearer_auth_middleware(create_sse_app(server=mcp, message_path='', sse_path='/sse')), host="0.0.0.0", port=8000)
