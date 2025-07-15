from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .chat import chat_with_memory
from .config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/chat")
async def chat_endpoint(
    message: dict,
    api_key: str = Header(..., alias="x-api-key")
):
    await verify_api_key(api_key)
    user_input = message.get("message")
    session_id = message.get("session_id")
    if not user_input or not session_id:
        raise HTTPException(400, "message and session_id required")
    reply = await chat_with_memory(user_input, session_id)
    return {"reply": reply}