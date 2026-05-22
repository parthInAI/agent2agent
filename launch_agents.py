#!/usr/bin/env python3
"""
launch_agents.py
Launches all three provider agents in background subprocesses,
then runs the requester agent and shows output.

Usage:
    python launch_agents.py
"""

import subprocess
import time
import sys
import os
import signal
import requests

AGENTS = [
    {"mode": "summarize",  "port": 8001},
    {"mode": "generate",   "port": 8002},
    {"mode": "analyze",    "port": 8003},
]

procs = []


def wait_for_agent(port: int, timeout: int = 15) -> bool:
    """Poll until the agent's /health endpoint responds."""
    for _ in range(timeout * 2):
        try:
            r = requests.get(f"http://localhost:{port}/health", timeout=1)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def shutdown(sig=None, frame=None):
    print("\n🛑  Shutting down all agents...")
    for p in procs:
        p.terminate()
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

print("\n🚀  Launching provider agents...")

for agent in AGENTS:
    cmd = [sys.executable, "agent_provider.py", agent["mode"], str(agent["port"])]
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    procs.append(p)
    print(f"   ✅  {agent['mode']:12s} agent → port {agent['port']}  (PID {p.pid})")

print("\n⏳  Waiting for agents to be ready...")
all_ready = True
for agent in AGENTS:
    ready = wait_for_agent(agent["port"])
    status = "✅ ready" if ready else "❌ timeout"
    print(f"   Port {agent['port']}  {status}")
    if not ready:
        all_ready = False

if not all_ready:
    print("\n⚠️  Some agents failed to start. Check for port conflicts.")
    shutdown()

print("\n" + "─" * 60)
print("  Running requester agent...")
print("─" * 60)

# Run requester in foreground so output is visible
subprocess.run([sys.executable, "agent_requester.py"])

print("\n🛑  Demo complete. Press Ctrl+C to stop provider agents.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    shutdown()
