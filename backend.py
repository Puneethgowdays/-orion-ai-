from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from llm_engine import query_llm
from personality import Personality

app = FastAPI(title="ORION AI Backend")

# Allow requests from anywhere (needed for mobile app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global personality instance
orion = Personality(
    humor=50,
    honesty=60,
    memory_limit=40,
    mode="serious"
)


# -------- Request/Response Models --------

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

class SetPersonalityRequest(BaseModel):
    humor: Optional[float] = None
    honesty: Optional[float] = None
    mode: Optional[str] = None


# -------- Routes --------

@app.get("/")
def root():
    return {"status": "ORION online", "personality": orion.summary()}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    user_message = request.message.strip()

    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    orion.remember(f"You: {user_message}")
    context = orion.build_context(orion.memory)
    final_prompt = (
        context
        + f"\nUser says: {user_message}\n"
        + "ORION response:"
    )

    ai_reply = query_llm(final_prompt)
    orion.remember(f"ORION: {ai_reply}")

    return ChatResponse(reply=ai_reply)


@app.get("/status")
def status():
    return {
        "humor": orion.humor,
        "honesty": orion.honesty,
        "mode": orion.mode,
        "memory_count": len(orion.memory),
        "memory_limit": orion.memory_limit
    }


@app.get("/memory")
def memory():
    return {"memory": orion.memory}


@app.post("/personality")
def set_personality(request: SetPersonalityRequest):
    messages = []
    if request.humor is not None:
        messages.append(orion.set_humor(request.humor))
    if request.honesty is not None:
        messages.append(orion.set_honesty(request.honesty))
    if request.mode is not None:
        messages.append(orion.set_mode(request.mode))
    return {"updated": messages, "personality": orion.summary()}


@app.delete("/memory")
def clear_memory():
    orion.memory = []
    return {"status": "Memory cleared."}