# locallama.py
import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from groq import Groq

# --- configuration ---------------------------------------------------------
load_dotenv()
# expect the key to be set either in the environment or a .env file
# (do **not** commit a real key to source control!).
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise RuntimeError(
        "GROQ_API_KEY not set – please add it to your environment or a .env file "
        "(`GROQ_API_KEY=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)."
    )

client = Groq(api_key=groq_api_key)

# --- FastAPI application ---------------------------------------------------
app = FastAPI(
    title="Groq LLM Server",
    version="1.0",
    description="Simple API backed by a Groq-powered chat model",
)


class TopicRequest(BaseModel):
    topic: str


def _run_prompt(prompt: str) -> str:
    """Helper that calls Groq and extracts the reply text."""
    try:
        resp = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-70b-versatile",
        )
        return resp.choices[0].message.content
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/groq")
async def groq_chat(req: TopicRequest):
    """Echo the user message through Groq."""
    return {"response": _run_prompt(req.topic)}


@app.post("/essay")
async def essay(req: TopicRequest):
    prompt = f"Write a clear, well-structured essay about '{req.topic}' in exactly 100 words."
    return {"response": _run_prompt(prompt)}


@app.post("/poem")
async def poem(req: TopicRequest):
    prompt = (
        f"Write me a poem about {req.topic} for a 5 years child with 100 words"
    )
    return {"response": _run_prompt(prompt)}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)


