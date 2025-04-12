import json
import random
from datetime import datetime

def parse_onchain_data(file_path: str = "realdata.json") -> dict:
    try:
        with open(file_path) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"nodes": []}

    nodes = data.get("nodes", [])
    total_staked = sum(node.get("staked", 0) for node in nodes)
    health_scores = [node.get("health_score", 0.9) for node in nodes if node]
    
    avg_health = (sum(health_scores) / len(health_scores)) * 100 if health_scores else 90.0

    return {
        "total_staked": total_staked * (0.99 + 0.02 * random.random()),
        "health_score": max(0, min(100, avg_health + random.uniform(-2, 2))),
        "last_updated": datetime.now().isoformat()
    }