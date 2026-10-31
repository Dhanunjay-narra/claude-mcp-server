import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.responses import JSONResponse
from starlette.routing import Route

mcp = FastMCP("YouTubeAutomationServer")

@mcp.tool()
def generate_youtube_idea(topic: str) -> str:
    """Returns a YouTube video concept based on a topic"""
    return f"Best video idea for '{topic}': 5 Secrets Nobody Tells You About {topic}!"

@mcp.tool()
def get_tags(topic: str) -> str:
    """Returns viral tags for the video"""
    return f"Tags: #{topic}, #{topic}Tutorial, #ViralVideo, #Trending"

# FastMCP SSE అప్లికేషన్
app = mcp.sse_app()

# రూట్ పాత్ (/) కి 404 రాకుండా రెస్పాన్స్ ఇవ్వడం
async def homepage(request):
    return JSONResponse({
        "status": "healthy",
        "message": "YouTube Automation MCP Server is running"
    })

# రూట్ పాత్‌ను అప్లికేషన్‌కు యాడ్ చేయడం
app.routes.insert(0, Route("/", endpoint=homepage))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)