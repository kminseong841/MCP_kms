from mcp.server.auth.provider import TokenVerifier, AccessToken

class SimpleTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        if token == "kms-secret-token":
            return AccessToken()
        return None