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
            
            
            logger.info("Successfully initialized DfManager")
            
        except Exception as e:
            logger.error(f"Error initializing DfManager: {str(e)}")
            raise
        
        
    def get_cleaned_df(self) -> pd.DataFrame:
        """Get the cleaned DataFrame."""
        try:
            preprocess_df = PreprocessDf(self.df)
            self.cleaned_df = preprocess_df.run()
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
            category_set = set()
            for category in self.df['category'].to_list():
                if isinstance(category, list):
                    for c in category:
                        if c:  # Only add non-empty categories
                            category_set.add(c)
            logger.debug(f"Found {len(category_set)} unique categories")
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
            concerns_set = set()
            for concerns in self.df['concerns'].to_list():
                if isinstance(concerns, list):
                    for concern in concerns:
                        if isinstance(concern, (list, tuple)) and concern:
                            concerns_set.add(concern[0])  # Add first element if it's a tuple/list
                        elif concern:  # Add the concern if it's a non-empty string
                            concerns_set.add(concern)
            logger.debug(f"Found {len(concerns_set)} unique concerns")
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
            ingredients_set = set()
            for ingredients in self.df['ingredients'].to_list():
                if isinstance(ingredients, list):
                    for ingredient in ingredients:
                        if isinstance(ingredient, (list, tuple)) and ingredient:
                            ingredients_set.add(ingredient[0])  # Add first element if it's a tuple/list
                        elif ingredient:  # Add the ingredient if it's a non-empty string
                            ingredients_set.add(ingredient)
            logger.debug(f"Found {len(ingredients_set)} unique ingredients")    
            return ingredients_set
        except Exception as e:
            logger.error(f"Error getting ingredients set: {str(e)}")
            raise   
    

if __name__ == "__main__":
    df_manager = DfManager("data/products.json")
    print(df_manager.get_ingredients_set())

    preprocess_df = PreprocessDf(df_manager.get_df())
    print(preprocess_df.run())
