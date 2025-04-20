"""
Product search and query tools for the Sales Chatbot.
"""

from typing import List, Dict, Optional
from langchain_core.tools import tool
import pandas as pd

from sales_chatbot.modules.helper.convert_json_to_df import convert_json_to_df

df = convert_json_to_df()

@tool
def search_products_by_concern(concern: str) -> List[Dict]:
    """
    Search for products by health/beauty concern (e.g., 'Hair loss', 'Dandruff', 'Eczema').
    
    Args:
        concern (str): The health or beauty concern to search for
    
    Returns:
        List[Dict]: A list of products addressing the specified concern
    """
    matches = df[df['concerns'].apply(
        lambda x: any(concern.lower() in c[0].lower() for c in x if c)
    )]
    return matches.to_dict('records')

@tool
def search_products_by_category(category: str) -> List[Dict]:
    """
    Search for products by category (e.g., 'Hair Care', 'Skin Care').
    
    Args:
        category (str): The category to search for
    
    Returns:
        List[Dict]: A list of products in the specified category
    """
    matches = df[df['category'].apply(
        lambda x: any(category.lower() in c.lower() for c in x)
    )]
    return matches.to_dict('records')

@tool
def search_products_by_name(name: str) -> List[Dict]:
    """
    Search for products by name.
    
    Args:
        name (str): The product name to search for (partial matches allowed)
    
    Returns:
        List[Dict]: A list of products matching the name query
    """
    matches = df[df['name'].str.lower().str.contains(name.lower())]
    return matches.to_dict('records')

@tool
def get_lowest_price_products(n: int = 5) -> List[Dict]:
    """
    Get the lowest priced products.
    
    Args:
        n (int): Number of products to return
    
    Returns:
        List[Dict]: A list of the n lowest priced products
    """
    return df.nsmallest(n, 'price').to_dict('records')

@tool
def get_highest_price_products(n: int = 5) -> List[Dict]:
    """
    Get the highest priced products.
    
    Args:
        n (int): Number of products to return
    
    Returns:
        List[Dict]: A list of the n highest priced products
    """
    return df.nlargest(n, 'price').to_dict('records')

@tool
def get_products_in_price_range(min_price: float, max_price: float) -> List[Dict]:
    """
    Get products within a specific price range.
    
    Args:
        min_price (float): Minimum price
        max_price (float): Maximum price
    
    Returns:
        List[Dict]: List of products within the specified price range
    """
    matches = df[(df['price'] >= min_price) & (df['price'] <= max_price)]
    return matches.to_dict('records')

tools = [
    search_products_by_concern,
    search_products_by_category,
    search_products_by_name,
    get_lowest_price_products,
    get_highest_price_products,
    get_products_in_price_range
] 