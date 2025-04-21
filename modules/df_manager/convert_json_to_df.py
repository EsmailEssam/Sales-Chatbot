import pandas as pd
import json
import os
from ..log_manager.log_manager import get_logger

# Initialize logger
logger = get_logger(__name__)

def convert_json_to_df(file_path: str) -> pd.DataFrame:
    """
    Convert a JSON file containing product data to a pandas DataFrame.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        pd.DataFrame: DataFrame containing the product data
        
    Raises:
        FileNotFoundError: If the JSON file doesn't exist
        ValueError: If the JSON file is empty or has invalid format
        Exception: For any other errors during conversion
    """
    try:
        logger.info(f"Converting JSON file to DataFrame: {file_path}")
        
        if not os.path.exists(file_path):
            logger.error(f"JSON file not found: {file_path}")
            raise FileNotFoundError(f"JSON file not found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            logger.debug("Reading JSON file")
            data = json.load(f)
            
        if not data or not isinstance(data, dict):
            logger.error("Invalid JSON data format")
            raise ValueError("JSON data must be a non-empty dictionary")
            
        if 'data' not in data or 'products' not in data['data']:
            logger.error("Missing required keys in JSON data")
            raise ValueError("JSON must contain 'data.products' structure")
            
        logger.debug("Creating DataFrame from JSON data")
        df = pd.DataFrame(data['data']['products'])
        
        logger.info(f"Successfully converted JSON to DataFrame with {len(df)} rows")
        return df
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format: {str(e)}")
        raise ValueError(f"Invalid JSON format: {str(e)}") from e
    except Exception as e:
        logger.error(f"Error converting JSON to DataFrame: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        logger.info("Starting JSON to DataFrame conversion test")
        file_path = os.path.join(os.getcwd(), 'Dataset', 'products.json')
        
        df = convert_json_to_df(file_path)
        logger.info("Test completed successfully")
        logger.debug(f"DataFrame head:\n{df.head()}")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise




