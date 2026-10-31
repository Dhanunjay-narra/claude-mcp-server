import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response
from starlette.routing import Route, Mount

# 1. MCP ఇన్‌స్టాన్స్
mcp = FastMCP("yt-custom-connector")

@mcp.tool()
def generate_youtube_idea(topic: str) -> str:
    """Returns a YouTube video concept based on a topic"""
    return f"Best video idea for '{topic}': 5 Secrets Nobody Tells You About {topic}!"

@mcp.tool()
def get_tags(topic: str) -> str:
    """Returns viral tags for the video"""
    return f"Tags: #{topic}, #{topic}Tutorial, #ViralVideo, #Trending"

# 2. SSE Sub-App
sse_sub_app = mcp.sse_app()

# 3. 405 ఎర్రర్ రాకుండా అన్ని మెథడ్స్‌కి సమాధానం ఇచ్చే రూట్ హ్యాండ్లర్
async def root_handler(request):
    if request.method == "HEAD":
        return Response(status_code=200)
    return JSONResponse({
        "status": "healthy",
        "service": "yt-custom-connector",
        "mcp_endpoint": "/sse"
    })

# 4. మెయిన్ Starlette యాప్ (CORS సపోర్ట్‌తో)
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = Starlette(
    routes=[
        Route("/", endpoint=root_handler, methods=["GET", "POST", "HEAD", "OPTIONS"]),
        Mount("/", app=sse_sub_app),  # /sse మరియు /messages రూట్లను మౌంట్ చేస్తుంది
    ],
    middleware=middleware,
)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)