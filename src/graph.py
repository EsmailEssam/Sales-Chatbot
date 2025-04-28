from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import tools_condition

# local imports
from .graph_blocks.nodes import run_sales_agent, tool_node, run_output_formatter
from .graph_blocks.state import AgentState
from .log_manager.log_manager import get_logger

# Initialize logger
logger = get_logger(__name__)

SALES_AGENT = "Sales_agent"
OUTPUT_FORMATTER = "Output_formatter"
ACT = "tools"

def get_graph():
    """
    Creates and returns a configured StateGraph for the sales agent application.
    
    Returns:
        StateGraph: A compiled graph with sales agent and tool nodes.
        
    Raises:
        Exception: If there's an error during graph creation or compilation.
    """
    try:
        logger.info("Creating new StateGraph")
        graph_builder = StateGraph(AgentState)
        
        # Add nodes
        logger.debug("Adding nodes to graph")
        graph_builder.add_node(SALES_AGENT, run_sales_agent)
        graph_builder.add_node(OUTPUT_FORMATTER, run_output_formatter)
        graph_builder.add_node(ACT, tool_node)
        
        # Set entry point
        logger.debug("Setting graph entry point")
        graph_builder.set_entry_point(SALES_AGENT)
        
        # Add edges
        logger.debug("Adding conditional edges")
        graph_builder.add_conditional_edges(
            SALES_AGENT,
            tools_condition,
            {
                ACT: ACT,
                OUTPUT_FORMATTER: OUTPUT_FORMATTER,
                # Add explicit mapping for END
                END: OUTPUT_FORMATTER
            }
        )
        
        logger.debug("Adding standard edges")
        graph_builder.add_edge(ACT, SALES_AGENT)
        graph_builder.add_edge(OUTPUT_FORMATTER, END)
        
        # Create checkpointer and compile
        logger.debug("Creating memory saver and compiling graph")
        checkpointer = MemorySaver()
        graph = graph_builder.compile(checkpointer=checkpointer)
        
        logger.info("Successfully created and compiled graph")
        return graph
        
    except Exception as e:
        logger.error(f"Error creating graph: {str(e)}")
        raise Exception(f"Failed to create graph: {str(e)}") from e