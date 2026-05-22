<div align="center">

# 🤖 Agent2Agent (A2A) Protocol — Multi-Agent System

**A modular multi-agent system demonstrating Google's Agent2Agent protocol**  
Built with FastAPI · TextBlob · Pydantic · Uvicorn

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Provider%20Agents-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![TextBlob](https://img.shields.io/badge/TextBlob-Sentiment%20NLP-F5A623?style=for-the-badge&logo=python&logoColor=white)](https://textblob.readthedocs.io)
[![Pydantic](https://img.shields.io/badge/Pydantic-Data%20Validation-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI%20Server-499848?style=for-the-badge&logo=gunicorn&logoColor=white)](https://uvicorn.org)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

</div>

---

## 📌 Overview

This project implements a **multi-agent system** following the **Agent2Agent (A2A) protocol** pattern. Three specialized provider agents expose REST API capabilities. A requester agent discovers them via an agent directory and dynamically delegates tasks based on capability matching.

```
Requester Agent
     │
     ├── capability: summarize      ──▶  SummarizationAgent   (port 8001)
     ├── capability: generate_text  ──▶  TextGeneratorAgent   (port 8002)
     └── capability: sentiment_analysis ▶ SentimentAnalysisAgent (port 8003)
```

---

## 🏗️ Architecture

```
agent_directory.json          ← Agent registry (name, capabilities, endpoint)
       │
agent_requester.py            ← Discovers agents, dispatches tasks by capability
       │
       ├── POST :8001/summarize   ──▶  agent_provider.py  [mode=summarize]
       ├── POST :8002/generate    ──▶  agent_provider.py  [mode=generate]
       └── POST :8003/analyze     ──▶  agent_provider.py  [mode=analyze]
```

---

## 🗂️ Project Structure

```
agent2agent/
├── agent_provider.py       # Universal provider agent (3 endpoints, 3 modes)
├── agent_requester.py      # Requester: discovers + delegates tasks
├── agent_directory.json    # Agent registry (A2A service discovery)
├── launch_agents.py        # One-command launcher for all agents
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| **API Framework** | [FastAPI](https://fastapi.tiangolo.com) | REST endpoints for each provider agent |
| **ASGI Server** | [Uvicorn](https://uvicorn.org) | Runs each provider agent instance |
| **NLP** | [TextBlob](https://textblob.readthedocs.io) | Sentiment polarity + subjectivity analysis |
| **Validation** | [Pydantic](https://docs.pydantic.dev) | Request/response schema enforcement |
| **Discovery** | JSON agent directory | A2A-style capability-based service registry |
| **Transport** | HTTP REST + JSON | Standardized A2A inter-agent communication |
| **Runtime** | Python 3.10+ | Core language |

---

## ⚡ Quick Start

### 1. Install dependencies

```bash
git clone https://github.com/parthInAI/agent2agent.git
cd agent2agent

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m textblob.download_corpora   # download TextBlob language data
```

### 2a. One-command launch (recommended)

```bash
python launch_agents.py
```

This starts all three provider agents, waits until they're ready, runs the requester, and streams the output.

### 2b. Manual launch (separate terminals)

```bash
# Terminal 1
python agent_provider.py summarize 8001

# Terminal 2
python agent_provider.py generate 8002

# Terminal 3
python agent_provider.py analyze 8003

# Terminal 4 — run after all three are up
python agent_requester.py
```

---

## 📤 Example Output

```
============================================================
  A2A Requester Agent — Task Dispatcher
============================================================

📤  Dispatching task → SummarizationAgent
    Endpoint  : http://localhost:8001/summarize
    Task ID   : 44d10dca-4a74-4f2a-a104-b3d1c2e9f5c7
    Input text: Google's Agent2Agent protocol enables AI agents...

✅  Provider  : SummarizationAgent
    Task ID   : 44d10dca-4a74-4f2a-a104-b3d1c2e9f5c7
    Status    : completed
    Result    : Google's Agent2Agent protocol enables AI agents to collaborate...

📤  Dispatching task → TextGeneratorAgent
    ...
    Result    : The future of AI agents [This is AI-generated continuation.]

📤  Dispatching task → SentimentAnalysisAgent
    ...
    Result    : {'sentiment': 'Positive', 'polarity': 0.625, 'subjectivity': 0.8}
```

---

## 🌐 API Reference

Each provider agent exposes the same base schema:

**Request:**
```json
{ "task_id": "<uuid>", "text": "<input text>" }
```

**Response:**
```json
{
  "provider": "SummarizationAgent",
  "task_id": "<uuid>",
  "status": "completed",
  "result": "<output>"
}
```

| Agent | Port | Endpoint | Capability |
|-------|------|----------|------------|
| SummarizationAgent | 8001 | `POST /summarize` | `summarize` |
| TextGeneratorAgent | 8002 | `POST /generate` | `generate_text` |
| SentimentAnalysisAgent | 8003 | `POST /analyze` | `sentiment_analysis` |

Interactive docs for each agent: `http://localhost:800{1,2,3}/docs`

---

## ✨ Key Concepts Demonstrated

- ✅ **Agent Discovery** — capability-based routing via `agent_directory.json`
- ✅ **Task Delegation** — requester dynamically picks the right provider per task
- ✅ **Standardized Protocol** — all agents share the same JSON request/response schema
- ✅ **Multiple Capabilities** — NLP summarization, text generation, sentiment analysis
- ✅ **Modular Design** — one `agent_provider.py` powers all three agents via mode flag

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.
