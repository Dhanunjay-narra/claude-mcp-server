import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response
from starlette.routing import Route, Mount

# 1. FastMCP ఇన్‌స్టాన్స్
mcp = FastMCP("youtube-custom-connector")

@mcp.tool()
def generate_youtube_idea(topic: str) -> str:
    """Returns a YouTube video concept based on a topic"""
    return f"Best video idea for '{topic}': 5 Secrets Nobody Tells You About {topic}!"

@mcp.tool()
def get_tags(topic: str) -> str:
    """Returns viral tags for the video"""
    return f"Tags: #{topic}, #{topic}Tutorial, #ViralVideo, #Trending"

# 2. FastMCP యొక్క Streamable HTTP ASGI యాప్
mcp_sub_app = mcp.streamable_http_app()

# 3. Claude వెరిఫికేషన్ కోసం 200 OK ఇచ్చే రెస్పాన్స్ (421 / 404 రాకుండా చేస్తుంది)
async def health_check(request):
    if request.method == "HEAD":
        return Response(status_code=200)
    return JSONResponse({
        "status": "healthy",
        "service": "youtube-custom-connector",
        "endpoints": ["/", "/mcp"]
    })

# 4. CORS మిడిల్‌వేర్
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

# 5. మెయిన్ స్టార్లెట్ అప్లికేషన్
app = Starlette(
    routes=[
        Route("/", endpoint=health_check, methods=["GET", "POST", "HEAD", "OPTIONS"]),
        Mount("/mcp", app=mcp_sub_app),  # /mcp పాత్‌ను నేరుగా మౌంట్ చేస్తుంది
        Mount("/", app=mcp_sub_app),     # రూట్ పాత్‌ను కూడా హ్యాండిల్ చేస్తుంది
    ],
    middleware=middleware,
)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)