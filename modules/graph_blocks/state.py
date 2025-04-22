from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from ..log_manager.log_manager import get_logger

# Initialize logger
logger = get_logger(__name__)

# Define a custom dictionary type to represent the state of the agent.
class AgentState(TypedDict):
    """
    Represents the state of the sales agent in the conversation graph.
    
    Attributes:
        messages (Annotated[list, add_messages]): A list of conversation messages 
            that can be appended to using the add_messages annotation.
    """
    messages: Annotated[list, add_messages]
    available_concerns: set
    available_categories: set
    available_ingredients: set

logger.debug("AgentState class defined with messages field")


