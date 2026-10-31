import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

# MCP సర్వర్ సెటప్
mcp = FastMCP("youtube-custom-connector")

@mcp.tool()
def generate_youtube_idea(topic: str) -> str:
    """Returns a YouTube video concept based on a topic"""
    return f"Best video idea for '{topic}': 5 Secrets Nobody Tells You About {topic}!"

@mcp.tool()
def get_tags(topic: str) -> str:
    """Returns viral tags for the video"""
    return f"Tags: #{topic}, #{topic}Tutorial, #ViralVideo, #Trending"

# Streamable HTTP ASGI యాప్
app = mcp.streamable_http_app()

# Claude వెరిఫికేషన్ కోసం 200 OK ఇచ్చే రూట్ హ్యాండ్లర్ (405 రాకుండా చేస్తుంది)
async def health_check(request):
    if request.method == "HEAD":
        return Response(status_code=200)
    return JSONResponse({
        "status": "healthy",
        "service": "youtube-custom-connector"
    })

# అప్లికేషన్‌కు రూట్ మరియు CORS జోడించడం
app.routes.insert(0, Route("/", endpoint=health_check, methods=["GET", "POST", "HEAD", "OPTIONS"]))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)