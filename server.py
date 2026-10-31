import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response
from starlette.routing import Route, Mount

# 1. MCP Server Definition
mcp = FastMCP("youtube-custom-connector")

@mcp.tool()
def generate_youtube_idea(topic: str) -> str:
    """Returns a YouTube video concept based on a topic"""
    return f"Best video idea for '{topic}': 5 Secrets Nobody Tells You About {topic}!"

@mcp.tool()
def get_tags(topic: str) -> str:
    """Returns viral tags for the video"""
    return f"Tags: #{topic}, #{topic}Tutorial, #ViralVideo, #Trending"

# 2. Native Streamable HTTP sub-application
mcp_sub_app = mcp.streamable_http_app()

# 3. Route Handlers
# Root path (/) Claude health check pass avvadaniki
async def root_health(request):
    if request.method == "HEAD":
        return Response(status_code=200)
    return JSONResponse({
        "status": "healthy",
        "service": "youtube-custom-connector"
    })

# OAuth probing ki explicit 404 ivvali (appude Claude "No sign-in" allow chesthundhi)
async def oauth_not_supported(request):
    return Response(status_code=404)

# 4. Global CORS Middleware setup
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
]

# 5. Starlette routing order (Priority order)
routes = [
    Route("/.well-known/{path:path}", endpoint=oauth_not_supported, methods=["GET", "POST", "HEAD"]),
    Route("/", endpoint=root_health, methods=["GET", "HEAD", "OPTIONS"]),
    Mount("/mcp", app=mcp_sub_app),
]

app = Starlette(routes=routes, middleware=middleware)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    # Render lo compulsory 0.0.0.0 bind cheyali
    uvicorn.run(app, host="0.0.0.0", port=port)