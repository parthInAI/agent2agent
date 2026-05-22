"""
agent_requester.py
Requester agent — discovers providers from agent_directory.json,
delegates tasks by capability, and prints results.

Usage:
    python agent_requester.py
"""

import requests
import json
import uuid
from datetime import datetime

# ── Load agent directory ──────────────────────────────────────────────────────

with open("agent_directory.json") as f:
    directory = json.load(f)

# ── Task queue ────────────────────────────────────────────────────────────────

tasks = [
    {
        "capability": "summarize",
        "text": (
            "Google's Agent2Agent protocol enables AI agents to collaborate "
            "effectively and share tasks securely within multi-agent environments."
        ),
    },
    {
        "capability": "generate_text",
        "text": "The future of AI agents",
    },
    {
        "capability": "sentiment_analysis",
        "text": "I'm thrilled with the results of using the new Agent2Agent protocol!",
    },
]

# ── Dispatch ──────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("  A2A Requester Agent — Task Dispatcher")
print("  Started:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 60)

for task_info in tasks:
    capability = task_info["capability"]

    # Discover the right provider
    provider = next(
        (agent for agent in directory["agents"] if capability in agent["capabilities"]),
        None,
    )

    if not provider:
        print(f"\n⚠️  No provider found for capability: '{capability}'")
        continue

    payload = {
        "task_id": str(uuid.uuid4()),
        "text": task_info["text"],
    }

    print(f"\n📤  Dispatching task → {provider['name']}")
    print(f"    Endpoint  : {provider['endpoint']}")
    print(f"    Task ID   : {payload['task_id']}")
    print(f"    Input text: {task_info['text'][:60]}{'...' if len(task_info['text']) > 60 else ''}")

    try:
        response = requests.post(provider["endpoint"], json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()
            print(f"\n✅  Provider  : {result['provider']}")
            print(f"    Task ID   : {result['task_id']}")
            print(f"    Status    : {result['status']}")
            print(f"    Result    : {result['result']}")
        else:
            print(f"\n❌  Error from {provider['name']} — HTTP {response.status_code}")
            print(f"    Response  : {response.text}")

    except requests.exceptions.ConnectionError:
        print(f"\n❌  Could not connect to {provider['name']} at {provider['endpoint']}")
        print(f"    Make sure the provider is running on port {provider['port']}")
    except requests.exceptions.Timeout:
        print(f"\n❌  Timeout contacting {provider['name']}")

print("\n" + "=" * 60)
print("  All tasks dispatched.")
print("=" * 60 + "\n")
