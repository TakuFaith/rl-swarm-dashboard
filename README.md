# RL-SWARM-DASHBOARD

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Next.js](https://img.shields.io/badge/Next.js-13.4+-black?logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green?logo=fastapi)](https://fastapi.tiangolo.com)

**Visualize collective reinforcement learning in decentralized AI systems**  
Built on Gensyn's RL Swarm research with real-time data integration.

![SwarmSight Demo](https://github.com/your-username/SwarmSight/blob/main/public/demo.gif?raw=true)

## ✨ Features

- **3D Swarm Personality Visualization**  
  Nodes color-coded by exploration/exploitation behavior
- **Shapley Value Analysis**  
  Quantifies individual node contributions to swarm success
- **Interactive Sandbox**  
  Simulate swarm mergers and predict performance
- **Real Gensyn Data Integration**  
  Connects to [RL Swarm research](https://github.com/gensyn-ai/paper-rl-swarm)

## 🛠️ Tech Stack

| Component       | Technology                          |
|-----------------|-------------------------------------|
| Frontend        | Next.js, Three.js, D3.js, Apollo Client |
| Backend         | FastAPI, The Graph, PyTorch         |
| Data Processing | Shapley values, PCA                 |
| Deployment      | Vercel + Docker                     |

## 🚀 Quick Start

### For Frontend Developers
```bash
git clone https://github.com/your-username/SwarmSight.git
cd SwarmSight/frontend
npm install
npm run dev
