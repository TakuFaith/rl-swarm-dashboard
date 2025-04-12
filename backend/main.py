from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .data_loader import load_node_data

from .onchain_parser import get_onchain_activity

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/nodes")
def get_nodes():
    return load_node_data()

@app.get("/api/node/{node_id}")
def get_node(node_id: str):
    nodes = load_node_data()
    for node in nodes:
        if node["node_id"] == node_id:
            return node
    return {"error": "Node not found"}

@app.get("/api/swarm/performance")
def get_swarm_performance():
    nodes = load_node_data()
    total_reward = sum(node["average_reward"] for node in nodes)
    average_reward = total_reward / len(nodes) if nodes else 0
    return {"average_reward": average_reward, "total_nodes": len(nodes)}

@app.get("/api/onchain")
def get_onchain():
    return get_onchain_activity()
