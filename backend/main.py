from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import asyncio
import random
from datetime import datetime
from data_loader import load_swarm_data

# Dummy parser if onchain_parser not available
def parse_onchain_data():
    return {"onchain_metric": random.random()}

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Broadcast error: {e}")

manager = ConnectionManager()

# Real-time Swarm Simulation Loop
async def simulate_swarm_updates():
    while True:
        try:
            # 1. Load and process data
            onchain_data = parse_onchain_data()
            swarm_data = load_swarm_data()

            # 2. Simulate small updates
            updated_data = {
                "timestamp": datetime.now().isoformat(),
                "onchain": onchain_data,
                "total_nodes": swarm_data["total_nodes"],
                "average_reward": swarm_data["average_reward"] * (0.99 + 0.02 * random.random()),
                "nodes": [
                    {
                        **node,
                        "reward": node["reward"] * (0.98 + 0.04 * random.random()),
                        "last_active": datetime.now().isoformat()
                    }
                    for node in swarm_data["nodes"]
                ]
            }

            # 3. Broadcast
            await manager.broadcast(updated_data)
            await asyncio.sleep(2)

        except Exception as e:
            print(f"Simulation error: {e}")
            await asyncio.sleep(5)

# WebSocket Route
@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keeps connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# HTTP GET Fallback Endpoint
@app.get("/api/swarm")
async def get_swarm_data():
    return {
        **load_swarm_data(),
        "timestamp": datetime.now().isoformat()
    }

# Launch simulation on app startup
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(simulate_swarm_updates())

# Run app using uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
