# local imports
from modules.graph import get_graph
from modules.log_manager.log_manager import get_logger
from modules.df_manager.df_manager import DfManager
import os
# Initialize logger
logger = get_logger(__name__)

try:
    logger.info("Initializing graph")
    graph = get_graph()
    logger.info("Graph initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize graph: {str(e)}")
    raise

def get_answer(user_input):
    try:
        if not user_input or not isinstance(user_input, str):
            logger.error(f"Invalid user input: {user_input}")
            raise ValueError("User input must be a non-empty string")
            
        logger.info(f"Processing user input: {user_input}")
        config = {"configurable": {"thread_id": "1"}}
        df_manager = DfManager(os.path.join( 'Dataset', 'products.json'))
        
        available_concerns = df_manager.get_concerns_set()
        available_categories = df_manager.get_category_set()
        available_ingredients = df_manager.get_ingredients_set()
        logger.info(f"Available concerns: {available_concerns}")
        logger.info(f"Available categories: {available_categories}")
        logger.info("Starting graph stream")
        events = graph.stream(
            {'messages': [('user', user_input)], 'available_concerns': available_concerns, 'available_categories': available_categories, 'available_ingredients': available_ingredients},
            config,
            stream_mode='values',
        )
        
        event = None
        for event in events:
            try:
                event['messages'][-1].pretty_print()
                logger.debug(f"Processed message: {event['messages'][-1].content[:100]}...")
            except Exception as e:
                logger.warning(f"Error pretty printing message: {str(e)}")
        
        if event is None:
            logger.error("No response generated from graph")
            raise Exception("Failed to generate response")
            
        logger.info("Successfully generated response")
        return event
        
    except ValueError as e:
        logger.error(f"ValueError in get_answer: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error in get_answer: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        logger.info("Starting main program")
        user_input = "عاوز حاجه لتساقط الشعر؟"
        logger.info(f"Test input: {user_input}")
        
        event = get_answer(user_input)
        
        logger.info("Test response received")
        logger.debug("*" * 50)
        logger.debug(event['messages'][-1].content)
        logger.debug("*" * 50)
        
       
        
    except Exception as e:
        logger.error(f"Main program error: {str(e)}")
        raise





