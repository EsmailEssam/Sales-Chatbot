from typing import Annotated, TypedDict  # Importing type hinting utilities.
from langgraph.graph.message import add_messages

# Define a custom dictionary type to represent the state of the agent.
class AgentState(TypedDict):
    messages : Annotated[list, add_messages]


