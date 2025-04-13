# RL-SWARM-DASHBOARD

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Next.js](https://img.shields.io/badge/Next.js-13.4+-black?logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green?logo=fastapi)](https://fastapi.tiangolo.com)
 ## Project Overview
The RL Swarm Dashboard is a visualization tool for monitoring decentralized collective learning systems. It provides real-time insights into node performance, reward distribution, and overall swarm health in reinforcement learning environments.

Key Features:
- Real-time monitoring of node rewards and performance
- Swarm health and staking metrics visualization
- Node distribution analysis by reward ranges
- Simulation mode for testing different scenarios
- **Real Gensyn Data Integration**  
  Connects to [RL Swarm research](https://github.com/gensyn-ai/paper-rl-swarm)

## 🛠️ Tech Stack

| Component       | Technology                          |
|-----------------|-------------------------------------|
| Frontend        | HTML5, TAILWIND.CSS, JAVASCRIPT, CHART.JS |
| Backend         | FastAPI, Python,        |
| Data Processing | Shapley values, PCA                 |                 
# OTHER TOOLS
VSCODE for editing
JSON for data simulation
## 🚀 Quick Start

### For Frontend Developers
Before you start make sure you have uvicorn and websockets installed
```bash
git clone https://github.com/your-username/rl-swarm-dashboard.git
cd rl-swarm-dashboard/frontend
npm install
npm run dev
### Set up Python environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt


FUTURE DEVELOPMENT
🌐 Integration with real-time decentralized networks like Swarm or Filecoin

📈 Historical data logging and analytics

📡 WebSocket support for live updates

📱 Responsive mobile-friendly layout

🔒 Authentication for secure monitoring
