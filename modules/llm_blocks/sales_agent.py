from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from ..log_manager.log_manager import get_logger

# Initialize logger
logger = get_logger(__name__)

# Local importing
from tools.df_tools import tools

try:
    # Load environment variables
    logger.info("Loading environment variables")
    load_dotenv()

    # Get API key from environment variables
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        logger.error("GEMINI_API_KEY not found in environment variables")
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    logger.info("Successfully loaded API key")

    # Initialize LLM (Google Gemini)
    logger.info("Initializing Google Gemini LLM")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.0,
        api_key=api_key
    )
    logger.info("Successfully initialized LLM")

    logger.debug("Binding tools to LLM")
    llm_with_tools = llm.bind_tools(tools=tools)
    logger.info("Successfully bound tools to LLM")

except Exception as e:
    logger.error(f"Error during initialization: {str(e)}")
    raise

def Sales_agent():
    """
    Sales expert node that processes customer queries and suggests beauty and cosmetic products.
    Has superior ability to convince customers to buy.
    
    Returns:
        Chain: A langchain chain that processes customer queries
        
    Raises:
        Exception: If there's an error creating the chain
    """
    try:
        logger.info("Creating sales agent chain")
        
        prompt_template_path = os.path.join(  "prompts", 'sales_agent_prompt.txt')
        
        with open(prompt_template_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
        
        logger.debug("Creating chat prompt template")
        prompt = ChatPromptTemplate.from_template(
            prompt_template
        )
        
        logger.debug("Creating chain with prompt and LLM")
        chain = prompt | llm_with_tools
        
        logger.info("Successfully created sales agent chain")
        return chain
        
    except Exception as e:
        logger.error(f"Error creating sales agent chain: {str(e)}")
        raise Exception(f"Failed to create sales agent chain: {str(e)}") from e

if __name__ == "__main__":
    try:
        logger.info("Starting sales agent test")
        # Example input query
        user_query = "ايه ارخص منتج عندك؟"
        logger.info(f"Test query: {user_query}")
        
        agent = Sales_agent()
        response = agent.invoke({"messages": [("user", user_query)]})
        
        logger.info("Test completed successfully")
        logger.debug(f"Test response: {response}")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

    