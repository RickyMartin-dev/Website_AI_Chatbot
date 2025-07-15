from fastapi import Header, HTTPException, Depends
from .configs import config

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != config.api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
