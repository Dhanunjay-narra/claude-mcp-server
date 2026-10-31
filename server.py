import os
import uvicorn
from mcp.server.fastmcp import FastMCP

# MCP సర్వర్ సెటప్
mcp = FastMCP("YouTubeAutomationServer")

@mcp.tool()
def generate_youtube_idea(topic: str) -> str:
    """Returns a YouTube video concept based on a topic"""
    return f"Best video idea for '{topic}': 5 Secrets Nobody Tells You About {topic}!"

@mcp.tool()
def get_tags(topic: str) -> str:
    """Returns viral tags for the video"""
    return f"Tags: #{topic}, #{topic}Tutorial, #ViralVideo, #Trending"

# FastMCP ASGI అప్లికేషన్
app = mcp.streamable_http_app()

if __name__ == "__main__":
    # Render డైనమిక్‌గా కేటాయించే పోర్ట్‌ను పొందడం
    port = int(os.getenv("PORT", 10000))
    # తప్పనిసరిగా 0.0.0.0 బైండ్ చేయాలి
    uvicorn.run(app, host="0.0.0.0", port=port)