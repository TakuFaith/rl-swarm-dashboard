import json
import os

def load_node_data():
    data_file = os.path.join(os.path.dirname(__file__), "realdata.json")
    with open(data_file, "r") as f:
        return json.load(f)
