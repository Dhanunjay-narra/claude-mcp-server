import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.responses import JSONResponse
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

# Streamable HTTP అప్లికేషన్
app = mcp.streamable_http_app()

# Claude హెల్త్ చెక్ కోసం రూట్ పాత్ (/) హ్యాండ్లర్ (GET & HEAD రెండింటినీ అలో చేస్తుంది)
async def health_check(request):
    return JSONResponse({
        "status": "healthy",
        "service": "youtube-custom-connector"
    })

app.routes.insert(0, Route("/", endpoint=health_check, methods=["GET", "HEAD"]))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)