# server.py
from fastmcp import FastMCP
from fastmcp.server.http import create_sse_app
from fastapi import Request, HTTPException
from fastapi import FastAPI
import uvicorn

API_KEY = "kms-secret-key"

app = FastAPI()
mcp = FastMCP("My MCP Server")

@app.middleware("http")
async def verify_api_keys(request: Request, call_next):
    api_key = request.headers.get("Authorization")
    if api_key != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="your authorization is failed")
    return await call_next(request)

app.mount('/sse', mcp.sse_app())


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
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
