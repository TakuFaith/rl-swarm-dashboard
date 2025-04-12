from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import random
from datetime import datetime
from data_loader import load_swarm_data
from onchain_parser import parse_onchain_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections = []
        self.simulation_active = False
        self.node_count = 5  # Default node count

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

async def generate_simulation_data():
    swarm_data = load_swarm_data()
    return {
        "timestamp": datetime.now().isoformat(),
        "total_nodes": manager.node_count,
        "total_staked": swarm_data["total_staked"] * (0.95 + 0.1 * random.random()),
        "average_reward": swarm_data["average_reward"] * (0.9 + 0.2 * random.random()),
        "average_health": swarm_data["average_health"] * (0.9 + 0.2 * random.random()),
        "nodes": [
            {
                **node,
                "reward": node["reward"] * (0.8 + 0.4 * random.random()),
                "health_score": max(0.0, min(1.0, node["health_score"] * (0.8 + 0.4 * random.random()))),
                "last_active": datetime.now().isoformat()
            }
            for node in swarm_data["nodes"][:manager.node_count]
        ]
    }

async def simulation_loop():
    while True:
        try:
            if manager.simulation_active:
                data = await generate_simulation_data()
                await manager.broadcast(data)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"Simulation error: {e}")
            await asyncio.sleep(5)

@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except:
        manager.disconnect(websocket)

@app.get("/api/swarm")
async def get_swarm():
    return load_swarm_data()

@app.post("/api/simulate")
async def start_simulation(node_count: int):
    manager.simulation_active = True
    manager.node_count = node_count
    return {"message": f"Simulation started with {node_count} nodes"}

@app.on_event("startup")
async def startup():
    asyncio.create_task(simulation_loop())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)