# filepath: server.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

try:
    from groq import Groq
except ImportError:
    print("Please install the Groq client: pip install groq")

# --- Load environment variables ---
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY not set. Please add it to your .env file "
        "like: GROQ_API_KEY=gsk_YOUR_API_KEY"
    )

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# --- FastAPI app ---
app = FastAPI(
    title="Groq LLM Server",
    version="1.0",
    description="FastAPI server with Groq-powered chat model"
)

class Topic(BaseModel):
    topic: str

def generate_text(prompt: str, model: str = "llama-3.1-mini") -> str:
    """
    Calls Groq API and returns the generated text.
    Includes debugging printouts for errors.
    """
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Groq API error:", e)  # This will show in the terminal
        raise HTTPException(status_code=500, detail=f"Groq API error: {e}")

# --- API endpoints ---
@app.post("/essay")
def essay(t: Topic):
    prompt = f"Write a clear, well-structured essay about '{t.topic}' in 100 words."
    return {"response": generate_text(prompt)}

@app.post("/poem")
def poem(t: Topic):
    prompt = f"Write a fun poem for a 5-year-old about '{t.topic}' in 100 words."
    return {"response": generate_text(prompt)}

@app.post("/groq")
def groq_chat(t: Topic):
    return {"response": generate_text(t.topic)}

# --- Run server ---
if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
