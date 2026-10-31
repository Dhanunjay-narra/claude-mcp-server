import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

app = FastAPI(title="youtube-custom-connector")

# CORS సెటప్
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Claude OAuth Probe చెక్స్ కి 404 ఇవ్వడం (status 200/421 అథెంటికేషన్ ఎర్రర్లు రావు)
@app.get("/.well-known/{path:path}")
@app.post("/.well-known/{path:path}")
@app.head("/.well-known/{path:path}")
async def reject_oauth(path: str):
    return Response(status_code=404)

# 2. బ్రౌజర్ & Render హెల్త్ చెక్ రెస్పాన్స్
@app.get("/")
@app.head("/")
async def root():
    return JSONResponse({
        "status": "healthy",
        "service": "youtube-custom-connector",
        "mcp_ready": True
    })

# 3. అధికారిక MCP టూల్స్ డెఫినిషన్
TOOLS = [
    {
        "name": "generate_youtube_idea",
        "description": "Returns a YouTube video concept based on a topic",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "The video topic"}
            },
            "required": ["topic"]
        }
    },
    {
        "name": "get_tags",
        "description": "Returns viral tags for the video",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "The video topic"}
            },
            "required": ["topic"]
        }
    }
]

# 4. MCP JSON-RPC హ్యాండ్లర్
@app.post("/")
@app.post("/mcp")
@app.post("/mcp/")
async def handle_mcp(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": None})

    req_id = body.get("id")
    method = body.get("method")
    params = body.get("params", {})

    # Claude సర్వర్ ప్రారంభించేటప్పుడు (Initialize Handshake)
    if method == "initialize":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {"listChanged": False}
                },
                "serverInfo": {
                    "name": "youtube-custom-connector",
                    "version": "1.0.0"
                }
            }
        })

    # క్లాడ్ నోటిఫికేషన్ పంపినప్పుడు
    elif method == "notifications/initialized":
        return Response(status_code=204)

    # టూల్స్ లిస్ట్ పంపడం
    elif method == "tools/list":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": TOOLS
            }
        })

    # క్లాడ్ చాట్ లో టూల్ కాల్ చేసినప్పుడు
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        topic = args.get("topic", "General")

        if tool_name == "generate_youtube_idea":
            text = f"Best video idea for '{topic}': 5 Secrets Nobody Tells You About {topic}!"
        elif tool_name == "get_tags":
            text = f"Tags: #{topic}, #{topic}Tutorial, #ViralVideo, #Trending"
        else:
            text = f"Unknown tool: {tool_name}"

        return JSONResponse({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [
                    {"type": "text", "text": text}
                ]
            }
        })

    # ఇతర మెథడ్స్
    return JSONResponse({
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method {method} not found"}
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)