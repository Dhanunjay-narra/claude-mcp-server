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

# 2. FastMCP కి చెందిన నేటివ్ ASGI Streamable HTTP యాప్
mcp_app = mcp.streamable_http_app()

# 3. బ్రౌజర్‌లో 'Not Found' రాకుండా మరియు Claude హెల్త్-చెక్ పాస్ అవ్వడానికి 200 OK హ్యాండ్లర్
async def homepage(request):
    if request.method == "HEAD":
        return Response(status_code=200)
    return JSONResponse({
        "status": "healthy",
        "service": "yt-custom-connector",
        "mcp_ready": True
    })

# 4. CORS మిడిల్‌వేర్
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
]

# 5. స్టార్లెట్ యాప్ కాన్ఫిగరేషన్
app = Starlette(
    routes=[
        Route("/", endpoint=homepage, methods=["GET", "POST", "HEAD", "OPTIONS"]),
        Mount("/mcp", app=mcp_app),
        Mount("/", app=mcp_app),
    ],
    middleware=middleware,
)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)