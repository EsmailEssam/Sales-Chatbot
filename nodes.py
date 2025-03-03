from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode
from react import react_agent_runnable

# local imports
from state import AgentState
from tools.df_tools import tools

load_dotenv()


def run_agent_reasoning_engine(state: AgentState):
    agent_outcome = react_agent_runnable.invoke(state)
    
    return {'agent_outcome': agent_outcome}
    
    
tool_executor = ToolNode(tools)
    
def execute_tools(state: AgentState):
    agent_action = state['agent_outcome']
    output = tool_executor
    
    # Fix the intermediate_steps structure to be a list of tuples
    # Each tuple should contain exactly (action, observation)
    return {'intermediate_steps': [(agent_action, str(output))]}