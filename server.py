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

# SSE ASGI అప్లికేషన్
app = mcp.sse_app()

# రూట్ పాత్ (/) కి వచ్చే వెరిఫికేషన్ రిక్వెస్ట్ కోసం 200 OK హ్యాండ్లర్
async def root_handler(request):
    return JSONResponse({
        "status": "ok",
        "service": "youtube-custom-connector"
    })

# రూట్ పాత్‌ను యాడ్ చేయడం వల్ల 404 / 421 రాదు
app.routes.insert(0, Route("/", endpoint=root_handler, methods=["GET", "POST", "HEAD"]))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    # 0.0.0.0 హోస్ట్ మరియు Render పోర్ట్‌తో Uvicorn రన్ చేయడం
    uvicorn.run(app, host="0.0.0.0", port=port)