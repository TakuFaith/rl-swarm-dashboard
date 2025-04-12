import json
import random
from datetime import datetime, timedelta

def parse_onchain_data():
    """Placeholder for actual on-chain data parsing"""
    return {
        "block_height": 123456,
        "network_status": "stable",
        "current_epoch": 42
    }

def load_swarm_data(file_path="realdata.json"):
    """Load swarm data with simulated real-time attributes"""
    with open(file_path) as f:
        data = json.load(f)
    
    # Add simulated node activity
    nodes = []
    for i, node in enumerate(data["nodes"]):
        nodes.append({
            "id": f"node-{i+1}",
            "reward": node["reward"] * (0.98 + 0.04 * random.random()),
            "staked": node["staked"],
            "last_active": (datetime.now() - timedelta(minutes=random.random() * 10)).isoformat(),
            "status": random.choice(["active", "syncing", "idle"])
        })
    
    return {
        "total_nodes": data["total_nodes"],
        "average_reward": sum(n["reward"] for n in nodes) / len(nodes),
        "nodes": nodes,
        **parse_onchain_data()  # Merge with on-chain data
    }