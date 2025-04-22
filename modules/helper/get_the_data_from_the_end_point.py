import requests
import json
import os
from typing import Dict, Optional
from ..log_manager.log_manager import get_logger

class ProductDataFetcher:
    """
    A class responsible for fetching product data from an API and saving it to a JSON file.
    
    Attributes:
        logger: Logger instance for recording operations
        default_api_url (str): Default URL for the products API endpoint
        default_save_dir (str): Default directory for saving the JSON file
    """
    
    def __init__(self, 
                 api_url: str = "https://nileva.meta-bytes.net/api/products",
                 save_dir: str = "Dataset"):
        """
        Initialize the ProductDataFetcher with optional API URL and save directory.
        
        Args:
            api_url (str): URL of the products API endpoint
            save_dir (str): Directory to save the JSON file
        """
        self.logger = get_logger(__name__)
        self.api_url = api_url
        self.save_dir = save_dir

    def fetch_data(self) -> Dict:
        """
        Fetch product data from the API.
        
        Returns:
            dict: The fetched product data
            
        Raises:
            requests.RequestException: If API request fails
            json.JSONDecodeError: If response contains invalid JSON
        """
        self.logger.info(f"Fetching products from API: {self.api_url}")
        response = requests.get(self.api_url)
        response.raise_for_status()
        products_data = response.json()
        self.logger.info(f"Successfully retrieved {len(products_data)} products")
        return products_data

    def save_data(self, data: Dict) -> str:
        """
        Save the product data to a JSON file.
        
        Args:
            data (dict): The product data to save
            
        Returns:
            str: Path where the file was saved
            
        Raises:
            OSError: If file cannot be saved
        """
        os.makedirs(self.save_dir, exist_ok=True)
        file_save_path = os.path.join(self.save_dir, 'products2.json')
        self.logger.debug(f"Saving data to: {file_save_path}")
        
        with open(file_save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        
        self.logger.info(f"Data successfully saved to {file_save_path}")
        return file_save_path

    def run(self) -> Dict:
        """
        Execute the complete process of fetching and saving product data.
        
        Returns:
            dict: The fetched and saved product data
            
        Raises:
            requests.RequestException: If API request fails
            json.JSONDecodeError: If response contains invalid JSON
            OSError: If file cannot be saved
            Exception: For any other errors
        """
        try:
            data = self.fetch_data()
            self.save_data(data)
            return data
        except (requests.RequestException, json.JSONDecodeError, OSError) as e:
            self.logger.error(f"Operation failed: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise



if __name__ == "__main__":
    try:
        logger = get_logger(__name__)
        logger.info("Starting product data fetch")
        fetcher = ProductDataFetcher()
        products = fetcher.run()
        logger.info("Product data fetch completed successfully")
    except Exception as e:
        logger.error(f"Product data fetch failed: {str(e)}")
        raise
