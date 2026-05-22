"""
agent_provider.py
Universal provider agent — handles summarization, text generation, and sentiment analysis.
Launch three instances on different ports:

    python agent_provider.py summarize  8001
    python agent_provider.py generate   8002
    python agent_provider.py analyze    8003
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from textblob import TextBlob
import sys
import uvicorn

app = FastAPI(title="A2A Provider Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

mode = sys.argv[1] if len(sys.argv) > 1 else "summarize"


# ── Schemas ───────────────────────────────────────────────────────────────────

class Task(BaseModel):
    task_id: str
    text: str


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "mode": mode}


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.post("/summarize")
def summarize(task: Task):
    """Truncate text to a 100-char summary."""
    summary = task.text[:100] + "..." if len(task.text) > 100 else task.text
    return {
        "provider": "SummarizationAgent",
        "task_id": task.task_id,
        "status": "completed",
        "result": summary,
    }


@app.post("/generate")
def generate_text(task: Task):
    """Append an AI-generated continuation to the input text."""
    generated_text = task.text + " [This is AI-generated continuation.]"
    return {
        "provider": "TextGeneratorAgent",
        "task_id": task.task_id,
        "status": "completed",
        "result": generated_text,
    }


@app.post("/analyze")
def sentiment_analysis(task: Task):
    """Run TextBlob sentiment analysis on the input text."""
    analysis = TextBlob(task.text).sentiment
    if analysis.polarity > 0:
        sentiment = "Positive"
    elif analysis.polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "provider": "SentimentAnalysisAgent",
        "task_id": task.task_id,
        "status": "completed",
        "result": {
            "sentiment": sentiment,
            "polarity": round(analysis.polarity, 4),
            "subjectivity": round(analysis.subjectivity, 4),
        },
    }


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8001
    print(f"\n🤖  Provider Agent [{mode}] starting on port {port}")
    uvicorn.run("agent_provider:app", host="0.0.0.0", port=port, reload=False)
