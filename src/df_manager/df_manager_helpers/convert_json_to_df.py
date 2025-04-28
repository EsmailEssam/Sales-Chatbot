from jsonschema import ValidationError
import pandas as pd
import json
import os
from ...log_manager.log_manager import get_logger
from ...schemas.products_from_end_point_schema import Product
from ...schemas.end_point_json_schema import EndPointJsonSchema

# Initialize logger
logger = get_logger(__name__)

class ConvertJsonToDf:
    """
    Convert a JSON file containing product data to a pandas DataFrame.
    
    Attributes:
        file_path (str): Path to the JSON file
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def read_json_file(self) -> dict:
        """
        Read the JSON file and return the data as a dictionary.
        
        Returns:
            dict: The data from the JSON file
            
        Raises:
            FileNotFoundError: If the JSON file doesn't exist
            ValueError: If the JSON file is empty or has invalid format
            Exception: For any other errors during reading
        """
        try:
            logger.info(f"Reading JSON file: {self.file_path}")
            
            if not os.path.exists(self.file_path):
                logger.error(f"JSON file not found: {self.file_path}")
                raise FileNotFoundError(f"JSON file not found: {self.file_path}")   
                
            with open(self.file_path, 'r', encoding='utf-8') as f:
                logger.debug("Reading JSON file")
                self.data = json.load(f)
                
                try:
                    self.validated_data = self._validate_end_point_json(self.data)
                except ValidationError as e:
                    logger.error(f"Validation error: {str(e)}")
                    raise
                
            if not self.validated_data or not isinstance(self.validated_data, dict):
                logger.error("Invalid JSON data format")
                raise ValueError("JSON data must be a non-empty dictionary")
                
            if 'data' not in self.validated_data or 'products' not in self.validated_data['data']:
                logger.error("Missing required keys in JSON data")
                raise ValueError("JSON must contain 'data.products' structure")
                
            logger.info(f"Successfully read JSON file: {self.file_path}")
            
        
        except FileNotFoundError as e:
            logger.error(f"File not found: {str(e)}")
            raise
        except ValueError as e:
            logger.error(f"Invalid JSON data: {str(e)}")
            raise
        
    def get_products_from_json(self) -> list:
        """
        Get the products from the JSON file.
        
        Returns:
            list: The products from the JSON file
        """
        try:
            return self.validated_data['data']['products']
        except Exception as e:
            logger.error(f"Error getting products from JSON: {str(e)}")
            raise
    
    def run(self) -> pd.DataFrame:
        """
        Convert the JSON data to a pandas DataFrame and return it.
        
        Returns:
            pd.DataFrame: DataFrame containing the product data
            
            
        Raises:
            Exception: For any other errors during conversion
        """
        try:
            logger.info(f"Converting JSON file to DataFrame: {self.file_path}")
            
            # First read and validate the JSON file
            self.read_json_file()
            # Then process the data
            products = self.get_products_from_json()
            validated_products = self._validate_products_keys(products)
            self.df = pd.DataFrame(validated_products)

            logger.info(f"Successfully converted JSON to DataFrame with {len(self.df)} rows")
            return self.df
        
        except Exception as e:
            logger.error(f"Error converting JSON to DataFrame: {str(e)}")
            raise
        
        
    def _validate_end_point_json(self, data: dict) -> dict:
        """
        Validate the end point JSON.
        
        Returns:
            dict: The validated end point JSON
        """
        try:
            return EndPointJsonSchema(**data).model_dump()
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            raise
    def _validate_products_keys (self, products: list) -> list:
        """
        Validate the keys of the products.
        
        Returns:
            list: The validated products
        """
        try:
            return [Product(**p).model_dump() for p in products]
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            raise
            

if __name__ == "__main__":
    try:
        logger.info("Starting JSON to DataFrame conversion test")
        file_path = os.path.join(os.getcwd(), 'Dataset', 'products.json')
        
        converter = ConvertJsonToDf(file_path)
        df = converter.run()
        logger.info("Test completed successfully")
        logger.debug(f"DataFrame head:\n{df.head()}")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise




