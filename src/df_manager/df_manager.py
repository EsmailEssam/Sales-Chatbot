import pandas as pd
from .df_manager_helpers.convert_json_to_df import ConvertJsonToDf
from ..log_manager.log_manager import get_logger
import os
from .df_manager_helpers.preprocess_df import PreprocessDf

# Initialize logger
logger = get_logger(__name__)


# TODO: edit the all get methods to use the cleaned df instead of the normal df
class DfManager:
    """
    Manages DataFrame operations for product data.
    
    Attributes:
        df (pd.DataFrame): The main DataFrame containing product data
    """
    
    def __init__(self, json_file_path: str):
        """
        Initialize DfManager with product data from JSON file.
        
        Args:
            json_file_path (str): Path to the JSON file containing product data
            
        Raises:
            FileNotFoundError: If JSON file doesn't exist
            ValueError: If data is invalid
            Exception: For other initialization errors
        """
        try:
            logger.info(f"Initializing DfManager with file: {json_file_path}")
            
            if not os.path.exists(json_file_path):
                logger.error(f"JSON file not found: {json_file_path}")
                raise FileNotFoundError(f"JSON file not found: {json_file_path}")
            
            self.df = ConvertJsonToDf(json_file_path).run()
            if self.df is None or self.df.empty:
                logger.error("Converted DataFrame is empty or None")
                raise ValueError("Failed to load product data - empty DataFrame")
            
            preprocess_df = PreprocessDf(self.df)
            self.cleaned_df = preprocess_df.run()
            
            logger.info("Successfully initialized DfManager")
            
        except Exception as e:
            logger.error(f"Error initializing DfManager: {str(e)}")
            raise
        
        
    def get_cleaned_df(self) -> pd.DataFrame:
        """Get the cleaned DataFrame."""
        try:
            
            return self.cleaned_df
        except Exception as e:
            logger.error(f"Error getting cleaned DataFrame: {str(e)}")
            raise

    def get_category_set(self) -> set:
        """
        Get unique set of categories.
        
        Returns:
            set: Unique categories
        """
        try:
            logger.debug("Getting category set")
            category_set = self._get_unique_values(self.cleaned_df, 'category')
            return category_set
        except Exception as e:
            logger.error(f"Error getting category set: {str(e)}")
            raise

    def get_concerns_set(self) -> set:
        """
        Get unique set of concerns.
        
        Returns:
            set: Unique concerns
        """
        try:
            logger.debug("Getting concerns set")
            concerns_set = self._get_unique_values(self.cleaned_df, 'concerns')
            return concerns_set
        except Exception as e:
            logger.error(f"Error getting concerns set: {str(e)}")
            raise
        
    def get_ingredients_set(self) -> set:
        """
        Get unique set of ingredients.
        
        Returns:
            set: Unique ingredients
        """
        try:
            logger.debug("Getting ingredients set")
            ingredients_set =  self._get_unique_values(self.cleaned_df, 'ingredients')
            logger.debug(f"Found {len(ingredients_set)} unique ingredients")    
            return ingredients_set
        except Exception as e:
            logger.error(f"Error getting ingredients set: {str(e)}")
            raise   

    def _get_unique_values(self,df, column):
        # Split comma-separated values, strip whitespace, and flatten the list
        return set(
            item.strip()
            for sublist in df[column].dropna().str.split(',')
            for item in sublist
        )

if __name__ == "__main__":
    df_manager = DfManager("data/products.json")
    print(df_manager.get_ingredients_set())

    preprocess_df = PreprocessDf(df_manager.get_df())
    print(preprocess_df.run())
