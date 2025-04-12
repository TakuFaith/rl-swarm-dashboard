import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Union

def load_swarm_data(file_path: str = "realdata.json") -> Dict[str, Union[int, float, List[Dict]]]:
    DEFAULT_DATA = {
        "nodes": [],
        "total_nodes": 0,
        "total_staked": 0
    }

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = DEFAULT_DATA

    if not isinstance(data.get("nodes"), list):
        data["nodes"] = []

    processed_nodes = []
    for node in data["nodes"]:
        processed_nodes.append({
            "id": node.get("id", "unknown"),
            "reward": float(node.get("reward", 0.0)),
            "staked": float(node.get("staked", 0.0)),
            "health_score": max(0.0, min(1.0, float(node.get("health_score", 0.9)))),
            "last_active": node.get("last_active") or (datetime.now() - timedelta(minutes=random.randint(0, 15))).isoformat(),
            "status": node.get("status", random.choice(["active", "syncing", "idle"]))
        })

    total_nodes = data.get("total_nodes", len(processed_nodes))
    total_staked = data.get("total_staked", sum(node["staked"] for node in processed_nodes))
    avg_reward = sum(node["reward"] for node in processed_nodes) / len(processed_nodes) if processed_nodes else 0.0
    avg_health = (sum(node["health_score"] for node in processed_nodes) / len(processed_nodes)) * 100 if processed_nodes else 90.0

    return {
        "total_nodes": total_nodes,
        "total_staked": total_staked,
        "average_reward": avg_reward,
        "average_health": avg_health,
        "nodes": processed_nodes
    }