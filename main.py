from dotenv import load_dotenv
from langchain_core.agents import AgentFinish
from langgraph.graph import END , StateGraph
from langgraph.checkpoint.memory import MemorySaver
load_dotenv()

# local imports
from nodes import run_agent_reasoning_engine , execute_tools
from state import AgentState


AGENT_REASON = "agent_reason"
ACT ="act"


def should_continue(state : AgentState) -> str:
    if isinstance(state['agent_outcome'] , AgentFinish):
        return END
    else:
        return ACT
    

flow = StateGraph(AgentState)

flow.add_node(AGENT_REASON, run_agent_reasoning_engine)
flow.set_entry_point(AGENT_REASON) 

flow.add_node(ACT, execute_tools)

flow.add_conditional_edges(
    AGENT_REASON ,
    should_continue
)
flow.add_edge(ACT , AGENT_REASON)    


checkpointer = MemorySaver()
app = flow.compile(checkpointer = checkpointer)


# print(app.get_graph().draw_mermaid())

if __name__ == "__main__":
    print("Hello, World!")
    config = {"configurable": {"thread_id": "1"}}
    # For Arabic query, make sure to properly handle it
    res = app.invoke(
        {
            "input": "ايه اغلي كتاب عندك",
            "intermediate_steps": []  # Initialize properly
        },
        config= config
        
    )
    
    print(res)






