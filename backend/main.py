from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import random
import json
import asyncio
from datetime import datetime
from onchain_parser import parse_onchain_data  # Your existing parser
from data_loader import load_swarm_data  # Your existing loader

app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

# Real-time Simulation Engine
async def simulate_swarm_updates():
    while True:
        try:
            # 1. Load fresh data
            onchain_data = parse_onchain_data()  # Use your existing parser
            swarm_data = load_swarm_data()  # Use your existing loader
            
            # 2. Merge with simulated changes
            updated_data = {
                "timestamp": datetime.now().isoformat(),
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
            
            # 3. Broadcast to all connected dashboards
            await manager.broadcast(updated_data)
            await asyncio.sleep(2)  # Update every 2 seconds
            
        except Exception as e:
            print(f"Simulation error: {e}")
            await asyncio.sleep(5)

# WebSocket Endpoint
@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# HTTP Fallback Endpoint
@app.get("/api/swarm")
async def get_swarm_data():
    return {
        **load_swarm_data(),
        "timestamp": datetime.now().isoformat()
    }

# Start simulation when app starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(simulate_swarm_updates())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)