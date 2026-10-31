import os
from mcp.server.fastmcp import FastMCP

# MCP సర్వర్ ఇన్‌స్టాన్స్
mcp = FastMCP("youtube-custom-connector")

@mcp.tool()
def generate_youtube_idea(topic: str) -> str:
    """Returns a YouTube video concept based on a topic"""
    return f"Best video idea for '{topic}': 5 Secrets Nobody Tells You About {topic}!"

@mcp.tool()
def get_tags(topic: str) -> str:
    """Returns viral tags for the video"""
    return f"Tags: #{topic}, #{topic}Tutorial, #ViralVideo, #Trending"

if __name__ == "__main__":
    # Render కేటాయించే PORT ని రీడ్ చేయడం
    port = int(os.getenv("PORT", 10000))
    # Streamable HTTP ట్రాన్స్‌పోర్ట్‌తో 0.0.0.0 హోస్ట్‌పై రన్ చేయడం
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)