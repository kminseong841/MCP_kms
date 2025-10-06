# server.py
from fastmcp import FastMCP

# 서버 인스턴스 생성
mcp = FastMCP("My MCP Server")

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
    # 기본은 stdio이지만, HTTP로 띄우면 클라이언트나 브라우저에서 접근하기 편합니다.
    # mcp.run()만 호출하면 stdio 전송을 사용합니다.
    # HTTP로 띄우고 싶으면 아래처럼 transport와 포트를 지정하세요.
    mcp.run(transport="http", host="0.0.0.0", port=8000)
