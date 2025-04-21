import requests
import json
import os
from ..log_manager.log_manager import get_logger

# Initialize logger
logger = get_logger(__name__)

def fetch_and_save_products(api_url: str = "https://nileva.meta-bytes.net/api/products", 
                          save_dir: str = "Dataset") -> dict:
    """
    Fetch product data from API and save to JSON file.
    
    Args:
        api_url (str): URL of the products API endpoint
        save_dir (str): Directory to save the JSON file
        
    Returns:
        dict: The fetched product data
        
    Raises:
        requests.RequestException: If API request fails
        OSError: If file cannot be saved
        Exception: For any other errors
    """
    try:
        logger.info(f"Fetching products from API: {api_url}")
        
        # Make GET request to the endpoint
        response = requests.get(api_url)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse JSON response
        products_data = response.json()
        logger.info(f"Successfully retrieved {len(products_data)} products")
        
        # Create save directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Save data to file
        file_save_path = os.path.join(save_dir, 'products.json')
        logger.debug(f"Saving data to: {file_save_path}")
        
        with open(file_save_path, 'w', encoding='utf-8') as f:
            json.dump(products_data, f, indent=4)
            
        logger.info(f"Data successfully saved to {file_save_path}")
        return products_data
        
    except requests.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON response: {str(e)}")
        raise
    except OSError as e:
        logger.error(f"Failed to save file: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        logger.info("Starting product data fetch")
        products = fetch_and_save_products()
        logger.info("Product data fetch completed successfully")
        
    except Exception as e:
        logger.error(f"Product data fetch failed: {str(e)}")
        raise
