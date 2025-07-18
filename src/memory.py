from typing import List, Dict
from langchain_core.messages import BaseMessage

class MemoryStore:
    def __init__(self):
        self._store: Dict[str, List[BaseMessage]] = {}

    def get_history(self, session_id: str) -> List[BaseMessage]:
        return self._store.get(session_id, [])

    def set_history(self, session_id: str, messages: List[BaseMessage]):
        self._store[session_id] = messages