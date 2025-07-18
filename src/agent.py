import uuid
from typing import List
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableLambda

from src.memory import MemoryStore
from src.bedrock import get_bedrock_response
from src.config import DEFAULT_SYSTEM_PROMPT

import logging
logger = logging.getLogger(__name__)

class ChatAgent:
    def __init__(self, system_prompt: str = DEFAULT_SYSTEM_PROMPT):
        self.system_prompt = system_prompt
        self.memory = MemoryStore()
        self.graph = self._build_graph()

    def _messages_to_prompt(self, messages: List[BaseMessage]) -> str:
        parts = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                continue
            role = "Human" if isinstance(msg, HumanMessage) else "Assistant"
            parts.append(f"\n\n{role}: {msg.content}")
        parts.append("\n\nAssistant:")
        return "".join(parts)

    def _build_graph(self):
        def node(state: dict) -> dict:
            session_id = state["session_id"]
            user_input = state["input"]
            messages = self.memory.get_history(session_id)

            if not messages or not isinstance(messages[0], SystemMessage):
                messages.insert(0, SystemMessage(content=self.system_prompt))

            messages.append(HumanMessage(content=user_input))
            prompt = self._messages_to_prompt(messages)

            response_text = get_bedrock_response(prompt)
            messages.append(AIMessage(content=response_text))
            self.memory.set_history(session_id, messages)

            # logger for testing
            logger.debug(f"🧠 State before chat node: {state}")
            logger.debug(f"📤 Response from Bedrock: {response_text}")

            return {
                "session_id": session_id,
                "messages": messages,
                "output": response_text
            }

        builder = StateGraph(state_schema=dict)
        builder.add_node("chat", RunnableLambda(node))
        builder.add_edge(START, "chat")
        builder.add_edge("chat", END)
        return builder.compile()

    def chat(self, user_input: str, session_id: str = None) -> dict:
        if not session_id:
            session_id = str(uuid.uuid4())
        return self.graph.invoke({"input": user_input, "session_id": session_id})
