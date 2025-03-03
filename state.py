import operator  # Importing the `operator` module to use built-in operators for processing.
from typing import Annotated, TypedDict, Union  # Importing type hinting utilities.

# Importing required LangChain core classes for defining the agent's action and final response.
from langchain_core.agents import AgentAction, AgentFinish  

# Define a custom dictionary type to represent the state of the agent.
class AgentState(TypedDict):
    # The user's input query to the agent.
    input: str  

    # The current state of the agent, which can be:
    # - `AgentAction`: Represents an action the agent is taking.
    # - `AgentFinish`: Represents the agent completing its reasoning process.
    # - `None`: Used for start and end nodes where no state is maintained.
    agent_outcome: Union[AgentAction, AgentFinish, None]  

    # A list of intermediate steps taken by the agent. Each step consists of:
    # - `AgentAction`: The action the agent performed.
    # - `str`: The output or response resulting from the action.
    # The `Annotated` type is used with `operator.add`, meaning lists will be concatenated when updating state.
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
