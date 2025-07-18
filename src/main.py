from fastapi import FastAPI, Request, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from src.config import API_KEY, ALLOWED_ORIGINS
from src.agent import ChatAgent
from src.logging import configure_logging

# Setup logging
configure_logging()
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ChatAgent instance
agent = ChatAgent()

# Input schema
class ChatInput(BaseModel):
    input: str
    session_id: str | None = None

# Dependency for API Key auth
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key

# POST /chat
@app.post("/chat")
async def chat_endpoint(
    payload: ChatInput,
    api_key: str = Depends(verify_api_key)
):
    try:
        logger.info(f"Incoming chat: {payload}")
        response = agent.chat(user_input=payload.input, session_id=payload.session_id)
        return {"response": response["output"]}
    except Exception as e:
        logger.exception("Error in /chat endpoint")
        raise HTTPException(status_code=500, detail=str(e))
