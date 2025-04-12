import json
import random
from datetime import datetime, timedelta

def load_swarm_data(file_path: str = "realdata.json") -> dict:
    DEFAULT_DATA = {
        "nodes": [],
        "total_nodes": 0,
        "total_staked": 0,
        "average_reward": 0.0,
        "average_health": 0.9
    }

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Using default data due to error: {str(e)}")
        data = DEFAULT_DATA

    processed_nodes = []
    for node in data.get("nodes", []):
        processed_nodes.append({
            "id": node.get("id", f"node-{random.randint(1000,9999)}"),
            "reward": float(node.get("reward", 0.0)),
            "staked": float(node.get("staked", 0.0)),
            "health_score": max(0.0, min(1.0, node.get("health_score", random.uniform(0.7, 1.0)))),
            "last_active": node.get("last_active") or (datetime.now() - timedelta(minutes=random.randint(0, 15))).isoformat(),
            "status": node.get("status", random.choice(["active", "syncing", "idle"]))
        })

    total_staked = sum(node["staked"] for node in processed_nodes)
    avg_reward = sum(node["reward"] for node in processed_nodes) / len(processed_nodes) if processed_nodes else 0.0
    avg_health = sum(node["health_score"] for node in processed_nodes) / len(processed_nodes) if processed_nodes else 0.9

    return {
        "total_nodes": len(processed_nodes),
        "total_staked": total_staked,
        "average_reward": avg_reward,
        "average_health": avg_health * 100,  # Convert to percentage
        "nodes": processed_nodes
    }