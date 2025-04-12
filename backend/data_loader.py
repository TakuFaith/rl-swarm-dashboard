import json
import random
from datetime import datetime, timedelta

def load_swarm_data(file_path: str = "realdata.json") -> dict:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"nodes": []}

    nodes = []
    for node in data.get("nodes", []):
        nodes.append({
            "id": node.get("id", f"node-{random.randint(1000,9999)}"),
            "reward": float(node.get("reward", random.uniform(5, 15))),
            "staked": float(node.get("staked", random.uniform(500, 2000))),
            "health_score": float(node.get("health_score", random.uniform(0.7, 1.0))),
            "status": node.get("status", random.choice(["active", "syncing", "idle"])),
            "last_active": node.get("last_active", (datetime.now() - timedelta(minutes=random.randint(0, 15))).isoformat())
        })

    return {
        "total_nodes": len(nodes),
        "total_staked": sum(node["staked"] for node in nodes),
        "average_reward": sum(node["reward"] for node in nodes) / len(nodes) if nodes else 0,
        "average_health": (sum(node["health_score"] for node in nodes) / len(nodes) * 100) if nodes else 0,
        "nodes": nodes
    }