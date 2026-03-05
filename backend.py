import os
import json
import base64
from datetime import datetime
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from llm_engine import query_llm, query_llm_with_image
from personality import Personality

app = FastAPI(title="ORION AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CHATS_FILE = "chats.json"

def load_chats():
    if os.path.exists(CHATS_FILE):
        with open(CHATS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_chats(chats):
    with open(CHATS_FILE, "w") as f:
        json.dump(chats, f, indent=2)

orion = Personality(humor=50, honesty=60, memory_limit=20, mode="serious")
chats = load_chats()


class ChatRequest(BaseModel):
    message: str
    chat_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    chat_id: str

class SetPersonalityRequest(BaseModel):
    humor: Optional[float] = None
    honesty: Optional[float] = None
    mode: Optional[str] = None


@app.get("/")
def root():
    return FileResponse("index.html")


@app.post("/chat/new")
def new_chat():
    chat_id = datetime.now().strftime("%Y%m%d%H%M%S")
    chats[chat_id] = {
        "id": chat_id,
        "title": "New Chat",
        "messages": [],
        "created": datetime.now().isoformat()
    }
    save_chats(chats)
    orion.memory = []
    return {"chat_id": chat_id, "title": "New Chat"}


@app.get("/chats")
def get_chats():
    return {"chats": list(chats.values())}


@app.get("/chats/{chat_id}")
def get_chat(chat_id: str):
    if chat_id not in chats:
        raise HTTPException(status_code=404, detail="Chat not found.")
    return chats[chat_id]


@app.delete("/chats/{chat_id}")
def delete_chat(chat_id: str):
    if chat_id not in chats:
        raise HTTPException(status_code=404, detail="Chat not found.")
    del chats[chat_id]
    save_chats(chats)
    return {"status": "Chat deleted."}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    user_message = request.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    chat_id = request.chat_id
    if not chat_id or chat_id not in chats:
        chat_id = datetime.now().strftime("%Y%m%d%H%M%S")
        chats[chat_id] = {
            "id": chat_id,
            "title": user_message[:40],
            "messages": [],
            "created": datetime.now().isoformat()
        }

    orion.memory = [f"{m['role'].upper()}: {m['content']}" for m in chats[chat_id]["messages"][-20:]]
    orion.remember(f"You: {user_message}")
    context = orion.build_context(orion.memory)
    final_prompt = context + f"\nUser says: {user_message}\nORION response:"
    ai_reply = query_llm(final_prompt)
    orion.remember(f"ORION: {ai_reply}")

    chats[chat_id]["messages"].append({"role": "user", "content": user_message, "time": datetime.now().isoformat()})
    chats[chat_id]["messages"].append({"role": "orion", "content": ai_reply, "time": datetime.now().isoformat()})
    save_chats(chats)

    return ChatResponse(reply=ai_reply, chat_id=chat_id)


@app.post("/chat/image")
async def chat_with_image(
    message: str = Form(""),
    chat_id: str = Form(""),
    file: UploadFile = File(...)
):
    """Handle image upload + optional text message."""
    # Read and encode image
    image_data = await file.read()
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    media_type = file.content_type or "image/jpeg"

    # Create chat if needed
    if not chat_id or chat_id not in chats:
        chat_id = datetime.now().strftime("%Y%m%d%H%M%S")
        chats[chat_id] = {
            "id": chat_id,
            "title": message[:40] if message else "Image Chat",
            "messages": [],
            "created": datetime.now().isoformat()
        }

    prompt = message.strip() if message.strip() else "What do you see in this image?"

    # Get vision response
    ai_reply = query_llm_with_image(prompt, image_base64, media_type)

    # Save to chat history
    chats[chat_id]["messages"].append({"role": "user", "content": f"[Image] {prompt}", "time": datetime.now().isoformat()})
    chats[chat_id]["messages"].append({"role": "orion", "content": ai_reply, "time": datetime.now().isoformat()})
    save_chats(chats)

    return {"reply": ai_reply, "chat_id": chat_id}


@app.get("/status")
def status():
    return {
        "humor": orion.humor,
        "honesty": orion.honesty,
        "mode": orion.mode,
        "memory_count": len(orion.memory),
        "total_chats": len(chats)
    }


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