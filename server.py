import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse

# Set your secret key (or load it from Render environment variables)
API_KEY = os.getenv("MCP_API_KEY", "my-super-secret-key-2026")

mcp = FastMCP("YouTubeAutomationServer")

@mcp.tool()
def generate_youtube_idea(topic: str) -> str:
    """Returns a YouTube video concept based on a topic"""
    return f"Best video idea for '{topic}': 5 Secrets Nobody Tells You About {topic}!"

@mcp.tool()
def get_tags(topic: str) -> str:
    """Returns viral tags for the video"""
    return f"Tags: #{topic}, #{topic}Tutorial, #ViralVideo, #Trending"

# Create the ASGI application
app = mcp.sse_app()

# Authentication Middleware
class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Allow preflight CORS OPTIONS requests if sent by the browser
        if request.method == "OPTIONS":
            return await call_next(request)

        client_key = request.headers.get("sd-api-key")
        if client_key != API_KEY:
            return PlainTextResponse("dhanunjay-server-yt-mcp", status_code=401)

        return await call_next(request)

app.add_middleware(APIKeyAuthMiddleware)

if __name__ == "__main__":
    # Render assigns a dynamic port via the PORT environment variable
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)