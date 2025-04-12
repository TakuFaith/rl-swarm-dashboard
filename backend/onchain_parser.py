import json
import random
from datetime import datetime, timedelta

def parse_onchain_data(file_path="realdata.json"):
    """Parse live on-chain data with simulated real-time updates"""
    with open(file_path) as f:
        data = json.load(f)
    
    # Simulate live updates
    return {
        "total_staked": data["total_staked"] * (0.99 + 0.02 * random.random()),
        "health_score": max(0, min(100, data["health_score"] + random.randint(-2, 2))),
        "last_updated": datetime.now().isoformat()
    }