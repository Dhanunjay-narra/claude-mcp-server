import os
import uvicorn
from mcp.server.fastmcp import FastMCP

# 1. MCP సర్వర్ క్రియేషన్
mcp = FastMCP(
    "yt-custom-connector",
    host="0.0.0.0"
)

@mcp.tool()
def generate_youtube_idea(topic: str) -> str:
    """Returns a YouTube video concept based on a topic"""
    return f"Best video idea for '{topic}': 5 Secrets Nobody Tells You About {topic}!"

@mcp.tool()
def get_tags(topic: str) -> str:
    """Returns viral tags for the video"""
    return f"Tags: #{topic}, #{topic}Tutorial, #ViralVideo, #Trending"

# 2. FastMCP కి చెందిన నేటివ్ ASGI Streamable HTTP యాప్
app = mcp.streamable_http_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    