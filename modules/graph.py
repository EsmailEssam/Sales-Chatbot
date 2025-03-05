from langgraph.graph import END , StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import  tools_condition

# local imports
from .nodes import run_sales_agent , tool_node
from .state import AgentState


SALES_AGENT = "Sales_agent"
ACT = "tools"

def get_graph():
    graph_builder = StateGraph(AgentState)
    graph_builder.add_node(SALES_AGENT , run_sales_agent)
    graph_builder.add_node(ACT, tool_node)

    graph_builder.set_entry_point(SALES_AGENT)  

    graph_builder.add_conditional_edges(
        SALES_AGENT,
        tools_condition
    )

    graph_builder.add_edge(  ACT  , SALES_AGENT  )
    graph_builder.add_edge(  SALES_AGENT ,  END  )
    checkpointer = MemorySaver()
    graph =  graph_builder.compile(checkpointer=checkpointer)
    
    return graph



