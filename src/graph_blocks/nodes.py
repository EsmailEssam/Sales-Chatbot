from langgraph.prebuilt import ToolNode

# local imports
from .state import AgentState
from .tools.df_tools import tools
from .llm_blocks.sales_agent import SalesAgent
from .llm_blocks.output_formatter import OutputFormatter
from ..log_manager.log_manager import get_logger
from ..df_manager.df_manager import DfManager

# Initialize logger
logger = get_logger(__name__)

def run_sales_agent(state: AgentState):
    """
    Run the sales agent with the given state.
    
    Args:
        state (AgentState): The current state containing messages
        
    Returns:
        dict: Response containing updated messages
        
    Raises:
        Exception: If there's an error during sales agent execution
    """
    try:
        logger.info("Running sales agent")
        logger.debug(f"Input state messages count: {len(state['messages'])}")
        
        sales_agent = SalesAgent()
        
        response = sales_agent.run({"messages": state["messages"] , "available_concerns": state["available_concerns"], "available_categories": state["available_categories"] , "available_ingredients": state["available_ingredients"]})
        
        logger.debug(f"Sales agent response received")
        return {"messages": response , "doctor_suggesions": response}
        
    except KeyError as e:
        logger.error(f"Invalid state format - missing key: {str(e)}")
        raise KeyError(f"State is missing required key: {str(e)}") from e
    except Exception as e:
        logger.error(f"Error running sales agent: {str(e)}")
        raise Exception(f"Failed to run sales agent: {str(e)}") from e
    
def run_output_formatter(state: AgentState):
    """
    Run the output formatter with the given state.
    
    Args:
        state (AgentState): The current state containing messages
        
    Returns:
        dict: Response containing updated messages
        
    Raises:
        Exception: If there's an error during output formatter execution
    """
    try:
        logger.info("Running output formatter")
        logger.debug(f"Input state messages count: {len(state['messages'])}")
        
        output_formatter = OutputFormatter()
        
        response = output_formatter.run({"doctor_suggesions": state["messages"][-2:] , "session_id": state["session_id"]})
        
        logger.debug(f"Output formatter response received")
        return {"output_formatter_response": response}
        
    except KeyError as e:
        logger.error(f"Invalid state format - missing key: {str(e)}")
        raise KeyError(f"State is missing required key: {str(e)}") from e
    except Exception as e:
        logger.error(f"Error running output formatter: {str(e)}")
        raise Exception(f"Failed to run output formatter: {str(e)}") from e
    


try:
    logger.info("Initializing tool node")
    tool_node = ToolNode(tools=tools)
    logger.info("Tool node initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize tool node: {str(e)}")
    raise Exception(f"Failed to initialize tool node: {str(e)}") from e

if __name__ == '__main__':
    try:
        logger.info("Starting nodes module test")
        test_state = AgentState(messages=[("user", "Test message")])
        response = run_sales_agent(test_state)
        logger.info("Test completed successfully")
        logger.debug(f"Test response: {response}")
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise
    