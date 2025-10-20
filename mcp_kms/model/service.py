from mcp import ClientSession
from mcp.client.sse import sse_client
from typing import Optional


API_KEY = "kms-secret-key"

class McpService:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.sse_client_cm = None
        self.ClientSession_cm = None
    
    async def start_session(self, server_url: str) -> ClientSession:
        self.sse_client_cm = sse_client(url=server_url, headers={"Authorization": f"Bearer {API_KEY}"})
        reader, writer = await self.sse_client_cm.__aenter__()

        self.ClientSession_cm = ClientSession(read_stream=reader, write_stream=writer)
        session = await self.ClientSession_cm.__aenter__()
        await session.initialize()
        
        self.session = session
        return session
    
    async def end_session(self):
        if self.ClientSession_cm is not None:
            await self.ClientSession_cm.__aexit__(None, None, None)
            self.session = None
            self.ClientSession_cm = None
        
        if self.sse_client_cm is not None:
            await self.sse_client_cm.__aexit__(None, None, None)
            self.sse_client_cm = None
        
        