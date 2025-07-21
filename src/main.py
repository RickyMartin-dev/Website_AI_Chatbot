from fastapi import FastAPI, Request, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
from src.config import API_KEY, ALLOWED_ORIGINS
from src.agent import ChatAgent
from src.logging import configure_logging

# Setup logging
configure_logging()
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)
# Initialize FastAPI
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
        # print(x_api_key, type(x_api_key), API_KEY, type(API_KEY))
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key

# POST /chat
@app.post("/chat")
@limiter.limit("10/minute")  # LIMIT: 10 requests per minute per IP
async def chat_endpoint(
    payload: ChatInput,
    request: Request,
    api_key: str = Depends(verify_api_key)
):
    origin = request.headers.get("origin")
    # print(origin)
    if origin not in ALLOWED_ORIGINS:
        logger.warning(f"Rejected origin: {origin}")
        raise HTTPException(status_code=403, detail="Forbidden origin")

    try:
        logger.info(f"Incoming chat: {payload}")
        response = agent.chat(user_input=payload.input, session_id=payload.session_id)
        return {"message": response["output"]}
    except Exception as e:
        logger.exception("Error in /chat endpoint")
        raise HTTPException(status_code=500, detail=str(e))
