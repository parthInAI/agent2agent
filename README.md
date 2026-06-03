# Agent2Agent Multi-Agent System

Three specialised AI agents that discover each other at runtime through a capability registry and delegate tasks with no central coordinator. Built following Google A2A protocol patterns. Adding a new agent requires zero changes to existing ones.

---

## The problem this solves

Most multi-agent demos use a central orchestrator that routes tasks. This creates a single point of failure and a bottleneck. This system uses peer-to-peer delegation: each agent announces its capabilities, and any agent can discover and call any other at runtime.

---

## How it works

```
Agent A (Research)          Agent B (Analysis)         Agent C (Writer)
     |                            |                           |
     |-- registers capabilities ->|                           |
     |                            |<-- registers capabilities-|
     |                            |                           |
     |         Capability Registry (runtime discovery)        |
     |                            |                           |
     |-- delegates sub-task ----->|                           |
     |                            |-- delegates sub-task ---->|
     |<-- result -----------------|<-- result ----------------|
```

No central coordinator. Each agent is independently deployable.

---

## Agents

| Agent | Responsibility |
|---|---|
| Research Agent | Retrieves and synthesises information from available sources |
| Analysis Agent | Processes retrieved data, extracts structured insights |
| Writer Agent | Formats and presents final output for the end user |

---

## Tech stack

| Component | Technology |
|---|---|
| Agent framework | Google A2A Protocol |
| API layer | FastAPI |
| Data validation | Pydantic |
| Sentiment analysis | TextBlob |
| Communication | REST (JSON) |

---

## Getting started

```bash
git clone https://github.com/parthInAI/agent2agent
cd agent2agent

pip install -r requirements.txt

# Start each agent on its own port
uvicorn agents.research:app --port 8001 &
uvicorn agents.analysis:app --port 8002 &
uvicorn agents.writer:app --port 8003 &

# Send a task to any agent
curl -X POST http://localhost:8001/task \
  -H "Content-Type: application/json" \
  -d '{"query": "Summarise the latest trends in LLM deployment"}'
```

---

## Key design decisions

**Why A2A protocol?** Google A2A is an open standard for agent-to-agent communication. Using it here means each agent exposes a standardised interface — any A2A-compatible agent from any framework can join the network.

**Why no central coordinator?** Removing the coordinator eliminates the single point of failure. Any agent can initiate a workflow. Any agent can be replaced or upgraded without touching the others.

**Why Pydantic for validation?** Every inter-agent message is validated against a strict schema before processing. This prevents malformed payloads from propagating silently through the system.

---

## Skills demonstrated

- Google A2A protocol implementation
- Peer-to-peer agent discovery and delegation
- FastAPI microservice design
- Runtime capability registry
- Modular, independently deployable architecture
- Structured inter-service communication

---

## Related projects

- [Agentic RAG + MCP](https://github.com/parthInAI/agentic-rag-mcp) — single-agent RAG with MCP tool-calling
- [Portfolio](https://parthinai.github.io/)
