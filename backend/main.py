from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import random
import json
from datetime import datetime
from typing import Dict, List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.simulation_active = False
        self.node_count = 12  # Default from realdata.json

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Broadcast error: {e}")

manager = ConnectionManager()

def load_swarm_data() -> Dict:
    with open("realdata.json") as f:
        data = json.load(f)
    
    processed_nodes = []
    for node in data["nodes"]:
        processed_nodes.append({
            "id": node["id"],
            "reward": node["reward"],
            "staked": node["staked"],
            "health_score": node["health_score"],
            "last_active": datetime.now().isoformat(),
            "status": node["status"]
        })
    
    return {
        "total_nodes": len(processed_nodes),
        "total_staked": sum(n["staked"] for n in processed_nodes),
        "average_reward": sum(n["reward"] for n in processed_nodes) / len(processed_nodes),
        "average_health": (sum(n["health_score"] for n in processed_nodes) / len(processed_nodes)) * 100,
        "nodes": processed_nodes
    }

async def simulate_swarm_updates():
    while True:
        if manager.simulation_active:
            swarm_data = load_swarm_data()
            updated_data = {
                "timestamp": datetime.now().isoformat(),
                "total_nodes": manager.node_count,
                "total_staked": swarm_data["total_staked"] * (0.95 + 0.1 * random.random()),
                "average_reward": swarm_data["average_reward"] * (0.98 + 0.04 * random.random()),
                "average_health": swarm_data["average_health"] * (0.97 + 0.06 * random.random()),
                "nodes": [
                    {
                        **node,
                        "reward": node["reward"] * (0.95 + 0.1 * random.random()),
                        "health_score": max(0, min(1, node["health_score"] * (0.95 + 0.1 * random.random())))
                    }
                    for node in swarm_data["nodes"][:manager.node_count]
                ]
            }
            await manager.broadcast(updated_data)
        await asyncio.sleep(2)

@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/swarm")
async def get_swarm_data():
    return load_swarm_data()

@app.post("/api/simulate")
async def start_simulation(node_count: int):
    manager.simulation_active = True
    manager.node_count = node_count
    return {"message": "Simulation started"}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(simulate_swarm_updates())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)