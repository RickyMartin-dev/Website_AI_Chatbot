from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver

# Seperate File so we can change logic later if need be

state_graph = StateGraph()
memory_saver = MemorySaver(storage="memory")