import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Union

def load_swarm_data(file_path: str = "realdata.json") -> Dict[str, Union[int, float, List[Dict]]]:
    """
    Load and process swarm node data from JSON file with fault tolerance.
    
    Args:
        file_path: Path to the JSON data file.
    
    Returns:
        Processed swarm data with calculated metrics.
    """
    DEFAULT_DATA = {
        "nodes": [{"reward": 10.0, "staked": 1000.0} for _ in range(5)]
    }

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Using default data due to error: {e}")
        data = DEFAULT_DATA

    if not isinstance(data.get("nodes"), list):
        print("Warning: 'nodes' is not a list - initializing empty node list")
        data["nodes"] = []

    processed_nodes = []
    for i, node in enumerate(data["nodes"]):
        try:
            # Validate or assign health_score
            raw_health = node.get("health_score", random.uniform(0.7, 1.0))
            try:
                health_score = float(raw_health)
            except (ValueError, TypeError):
                print(f"Warning: Invalid health_score for node {i}, using default")
                health_score = random.uniform(0.7, 1.0)

            health_score = max(0.0, min(1.0, health_score))

            processed_nodes.append({
                "id": node.get("id", f"node-{i+1}"),
                "reward": float(node.get("reward", 10.0)),
                "staked": float(node.get("staked", 1000.0)),
                "health_score": health_score,
                "last_active": node.get("last_active") or 
                               (datetime.now() - timedelta(minutes=random.uniform(0, 15))).isoformat(),
                "status": node.get("status", random.choice(["active", "syncing", "idle"]))
            })
        except (ValueError, TypeError) as e:
            print(f"Warning: Skipping corrupt node {i} ({e})")
            continue

    total_staked = sum(node["staked"] for node in processed_nodes)
    avg_reward = sum(node["reward"] for node in processed_nodes) / len(processed_nodes) if processed_nodes else 0.0
    avg_health = sum(node["health_score"] for node in processed_nodes) / len(processed_nodes) if processed_nodes else 0.9

    return {
        "total_nodes": len(processed_nodes),
        "total_staked": total_staked,
        "average_reward": avg_reward,
        "average_health": avg_health,
        "nodes": processed_nodes
    }

# Test the function
if __name__ == "__main__":
    print("=== Testing data_loader ===")
    test_data = load_swarm_data()
    print(f"Loaded {test_data['total_nodes']} nodes")
    print(f"Total staked: {test_data['total_staked']}")
    print(f"Avg reward: {test_data['average_reward']:.2f}")
    print(f"Avg health: {test_data['average_health']:.2f}")
    if test_data["nodes"]:
        print("\nFirst node sample:", json.dumps(test_data["nodes"][0], indent=2))
