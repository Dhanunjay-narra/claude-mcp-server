import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response
from starlette.routing import Route, Mount

# 1. FastMCP Instance
mcp = FastMCP("yt-custom-connector")

@mcp.tool()
def generate_youtube_idea(topic: str) -> str:
    """Returns a YouTube video concept based on a topic"""
    return f"Best video idea for '{topic}': 5 Secrets Nobody Tells You About {topic}!"

@mcp.tool()
def get_tags(topic: str) -> str:
    """Returns viral tags for the video"""
    return f"Tags: #{topic}, #{topic}Tutorial, #ViralVideo, #Trending"

# 2. FastMCP official Streamable HTTP ASGI app
mcp_app = mcp.streamable_http_app()

# 3. CORS Middleware
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
]

# 4. App creation: mcp_app direct ga root and /mcp rendu handle chestundi
# Ekkada OAuth fake routes levu, so Claude sign-in adagadu.
app = Starlette(
    routes=[
        Mount("/mcp", app=mcp_app),
        Mount("/", app=mcp_app),
    ],
    middleware=middleware,
)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)