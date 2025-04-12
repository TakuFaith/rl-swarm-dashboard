from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import time

app = FastAPI()

# Path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "../frontend"))
INDEX_HTML = os.path.join(FRONTEND_DIR, "index.html")
#ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")

# Mount static assets if folder exists
#if os.path.isdir(ASSETS_DIR):
    #app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve index.html
@app.get("/")
async def serve_index():
    return FileResponse(INDEX_HTML)

# Dummy Swarm Stats endpoint
@app.get("/api/swarm")
async def get_swarm_data():
    return {
        "total_nodes": 42,
        "average_reward": 18.5,
        "total_staked": 35000,
        "active_nodes": 30
    }

# Dummy nodes list
@app.get("/api/nodes")
async def get_nodes():
    return [
        {
            "node_id": f"node-{i}",
            "average_reward": round(i * 0.5 + 10, 2),
            "staked_tokens": i * 100,
            "last_active": "2025-04-12T12:00:00"
        } for i in range(1, 21)
    ]

# Dummy stream
@app.get("/api/stream")
async def stream_events():
    def event_generator():
        for i in range(5):
            yield f"data: New update {i}\n\n"
            time.sleep(2)
    return StreamingResponse(event_generator(), media_type="text/event-stream")
