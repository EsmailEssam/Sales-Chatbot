

from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import re
from dotenv import load_dotenv

from src.schemas.output_formatter import ResponseModel
from src.schemas.enums.llm_enums import GeminiMmodelName


# Load environment variables








from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from ...log_manager.log_manager import get_logger

# Initialize logger
logger = get_logger(__name__)

# Local importing
from ..tools.df_tools import tools

from .base import BaseLLMBlock

class OutputFormatter(BaseLLMBlock):
    """
    Sales expert LLM block that processes customer queries and suggests beauty and cosmetic products.
    Has superior ability to convince customers to buy.
    
    Inherits from BaseLLMBlock to maintain consistent structure with other LLM blocks.
    """
    
    def __init__(self, model_name: str = GeminiMmodelName.Gemini_1_5_flash.value, temperature: float = 0.0):
        """
        Initialize the sales agent.
        
        Args:
            model_name (str, optional): Name of the model to use. Defaults to "gemini-2.0-flash".
            temperature (float, optional): Temperature setting for generation. Defaults to 0.0.
        """
        super().__init__(model_name=model_name, temperature=temperature)
    
    def _validate_environment(self) -> None:
        """Validate that the GEMINI_API_KEY environment variable is present."""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            self.logger.error("GEMINI_API_KEY not found in environment variables")
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        self.logger.info("Successfully loaded API key")
    
    def _setup_llm(self) -> None:
        """Set up the Google Gemini LLM with tools."""
        try:
            self.logger.info("Initializing Google Gemini LLM")
            self.llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                temperature=self.temperature,
                api_key=self.api_key
            )
            self.logger.debug("Binding tools to LLM")
            self.llm = self.llm.bind_tools(tools=tools)
            self.logger.info("Successfully initialized LLM with tools")
        except Exception as e:
            self.logger.error(f"Failed to setup LLM: {str(e)}")
            raise
    
    def _setup_chain(self) -> None:
        """Set up the processing chain with the prompt template."""
        try:
            self.logger.info("Creating sales agent chain")
            parser = JsonOutputParser(pydantic_object=ResponseModel)
            
            prompt_template = self._load_prompt_template('output_formatter_prompt.txt')
            
            self.logger.debug("Creating chat prompt template")
            
            
            prompt = PromptTemplate(
                                template=prompt_template,
                                partial_variables={"format_instructions": parser.get_format_instructions()}
                            )
            
            self.logger.debug("Creating chain with prompt and LLM")
            self.chain = prompt | self.llm | parser
            
            self.logger.info("Successfully created sales agent chain")
        except Exception as e:
            self.logger.error(f"Failed to setup chain: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        # Example usage
        agent = SalesAgent()
        
        # Example input query
        user_query = "ايه ارخص منتج عندك؟"
        response = agent.invoke({"messages": [("user", user_query)]})
        
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

    