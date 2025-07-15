from fastapi import HTTPException
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda
import boto3
import time
from .memory import state_graph, memory_saver
from .logs import logger
from .config import settings

bedrock = boto3.client('bedrock-runtime', region_name=settings.AWS_REGION)
s3 = boto3.client('s3', region_name=settings.AWS_REGION)

def llm_invoke(prompt: str):
    response = bedrock.invoke_model(
        modelId=settings.AWS_BEDROCK_MODEL,
        inputText=prompt
    )
    return response.get('body')

llm = RunnableLambda(lambda prompt: llm_invoke(prompt))

async def chat_with_memory(user_input: str, session_id: str):
    history = state_graph.load(session_id) or []
    history.append(HumanMessage(content=user_input))

    reply = await llm.invoke(user_input)
    ai_msg = AIMessage(content=reply)
    history.append(ai_msg)
    state_graph.save(session_id, history)

    s3.put_object(
        Bucket=settings.S3_BUCKET,
        Key=f"chats/{session_id}/{int(time.time())}.json",
        Body=str([m.content for m in history])
    )

    logger.info(f"Session %s: %s -> %s", session_id, user_input, reply)
    return reply