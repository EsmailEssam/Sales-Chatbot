from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
import os
from ..log_manager.log_manager import get_logger

class BaseLLMBlock(ABC):
    """
    Abstract base class for LLM blocks that defines common functionality and structure.
    
    This class provides a template for creating different LLM-based processing blocks
    with consistent initialization, configuration, and execution patterns.
    """
    
    def __init__(self, model_name: str, temperature: float = 0.0):
        """
        Initialize the base LLM block.
        
        Args:
            model_name (str): Name of the LLM model to use
            temperature (float, optional): Temperature setting for the model. Defaults to 0.0.
        """
        self.logger = get_logger(self.__class__.__name__)
        self.model_name = model_name
        self.temperature = temperature
        self.llm = None
        self.chain = None
        self._initialize_environment()
        self._setup_llm()
        self._setup_chain()
    
    def _initialize_environment(self) -> None:
        """Initialize environment variables and configurations."""
        try:
            self.logger.info("Loading environment variables")
            load_dotenv()
            self._validate_environment()
        except Exception as e:
            self.logger.error(f"Environment initialization failed: {str(e)}")
            raise
    
    @abstractmethod
    def _validate_environment(self) -> None:
        """
        Validate that all required environment variables are present.
        Must be implemented by child classes.
        """
        pass
    
    def _load_prompt_template(self, prompt_file_name: str) -> str:
        """
        Load prompt template from file.
        
        Args:
            prompt_file_name (str): Name of the prompt template file
            
        Returns:
            str: Content of the prompt template
        """
        try:
            prompt_path = os.path.join("prompts", prompt_file_name)
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Failed to load prompt template: {str(e)}")
            raise
    
    @abstractmethod
    def _setup_llm(self) -> None:
        """
        Set up the specific LLM implementation.
        Must be implemented by child classes.
        """
        pass
    
    @abstractmethod
    def _setup_chain(self) -> None:
        """
        Set up the processing chain for the LLM block.
        Must be implemented by child classes.
        """
        pass
    
    
    def run(self, input_data: Dict[str, Any]) -> Any:
        """
        Process input data through the LLM chain.
        
        Args:
            input_data (Dict[str, Any]): Input data to process
            
        Returns:
            Any: Processed result from the chain
            
        Raises:
            Exception: If chain processing fails
        """
        try:
            self.logger.info("Processing input through chain")
            if not self.chain:
                raise ValueError("Chain not initialized")
            return self.chain.invoke(input_data)
        except Exception as e:
            self.logger.error(f"Chain processing failed: {str(e)}")
            raise 