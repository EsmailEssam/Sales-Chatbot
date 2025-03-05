
from langgraph.prebuilt import ToolNode


# local imports
from .state import AgentState
from tools.df_tools import tools
from .agents import Sales_agent


def run_sales_agent(state: AgentState):
    response = Sales_agent().invoke({"messages": state["messages"]})
    return {"messages": response}


tool_node =  ToolNode(tools= tools) 

  
if __name__ == '__main__':
    print("Hello, World!")
    
    run_ales_agent(AgentState)
    