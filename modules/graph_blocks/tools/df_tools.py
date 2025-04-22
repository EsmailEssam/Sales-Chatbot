import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # Add project root to Python path

from typing import List, Dict
from langchain_core.tools import tool 
import os
import pandas as pd
from modules.log_manager.log_manager import get_logger
from modules.df_manager.df_manager import DfManager

# Initialize logger
logger = get_logger(__name__)

try:
    logger.info("Loading product data")
    json_file_path = os.path.join(os.getcwd(), 'Dataset', 'products.json')
    
    if not os.path.exists(json_file_path):
        logger.error(f"Products file not found at {json_file_path}")
        raise FileNotFoundError(f"Products file not found at {json_file_path}")
        
    df_manager = DfManager(json_file_path)
    df = df_manager.get_cleaned_df()    
        
    logger.info(f"Successfully loaded {len(df)} products")
except Exception as e:
    logger.error(f"Error initializing product data: {str(e)}")
    raise

@tool
def query_products(search_term: str = None, category: str = None, concerns: str = None, 
                  price_min: float = None, price_max: float = None, has_ingredient: str = None,
                  best_seller: bool = None, new_arrived: bool = None) -> List[Dict]:
    """
    Query products based on various filters.
    
    Args:
        search_term (str, optional): Term to search in product names category ,  descriptions , concerns and ingredients 
        category (str, optional): Product category to filter by
        concerns (str, optional): Specific concerns to filter by
        price_min (float, optional): Minimum price filter
        price_max (float, optional): Maximum price filter
        has_ingredient (str, optional): Ingredient to filter by
        best_seller (bool, optional): Filter for best selling products
        new_arrived (bool, optional): Filter for newly arrived products
        
    Returns:
        List[Dict]: List of matching products with their details
    """
    try:
        result = df.copy()
        
        if search_term:
            search_term = search_term.lower()       
            result = result[result['search_text'].str.contains(search_term, na=False)]
        
        if category:
            result = result[result['category'].str.contains(category, case=False, na=False)]
            
        if concerns:
            result = result[result['concerns'].str.contains(concerns, case=False, na=False)]
        
        if price_min is not None:
            result = result[result['price'] >= price_min]
            
        if price_max is not None:
            result = result[result['price'] <= price_max]
        
        if has_ingredient:
            result = result[result['ingredients'].str.contains(has_ingredient, case=False, na=False)]
            
        if best_seller:
            result = result[result['best_seller'] == best_seller]
            
        if new_arrived:
            result = result[result['new_arrived'] == new_arrived]

        filtered_results = result[['product_id', 'name', 'description', 'ingredients', 'concerns', 'category', 'price', 'best_seller', 'new_arrived']]
        return filtered_results.to_dict('records')

    except Exception as e:
        logger.error(f"Error in query_products: {str(e)}")
        return [None]

# List of tools to be used with LangGraph
tools = [
    query_products
]

logger.debug("Initialized tools list with product search functions")