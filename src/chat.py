import uuid
from typing import List, Dict
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from src.agent import ChatAgent

import logging
logger = logging.getLogger(__name__)

class ChatSession:
    def __init__(self, agent: ChatAgent, session_id: str = None):
        self.agent = agent
        self.session_id = session_id or str(uuid.uuid4())

    def send(self, user_input: str) -> str:
        result = self.agent.chat(user_input, self.session_id)
        logger.info(f"📨 [{self.session_id}] User: {user_input}")
        logger.info(f"📨 [{self.session_id}] Assistant: {result}")
        return result["output"]

    def history(self) -> List[str]:
        return [
            f"{'You' if isinstance(m, HumanMessage) else 'Bot'}: {m.content}"
            for m in self.agent.memory.get_history(self.session_id)
            if isinstance(m, (HumanMessage, AIMessage))
        ]
