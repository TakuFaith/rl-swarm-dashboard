from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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

async def simulate_swarm_updates():
    while True:
        try:
            onchain_data = parse_onchain_data()
            swarm_data = load_swarm_data()

            updated_data = {
                "timestamp": datetime.now().isoformat(),
                "onchain": onchain_data,
                "total_nodes": swarm_data["total_nodes"],
                "total_staked": swarm_data["total_staked"],
                "average_reward": swarm_data["average_reward"] * (0.99 + 0.02 * random.random()),
                "average_health": swarm_data["average_health"],
                "nodes": [
                    {
                        **node,
                        "reward": node["reward"] * (0.98 + 0.04 * random.random()),
                        "last_active": datetime.now().isoformat()
                    }
                    for node in swarm_data["nodes"]
                ]
            }

            await manager.broadcast(updated_data)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"Simulation error: {e}")
            await asyncio.sleep(5)

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
    swarm_data = load_swarm_data()
    return {
        **swarm_data,
        "timestamp": datetime.now().isoformat()
    }

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(simulate_swarm_updates())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)