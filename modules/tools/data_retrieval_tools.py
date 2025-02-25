import os
from crewai.tools import tool
import pandas as pd
from typing import Dict, List, Optional
from typing import List, Dict

data_path = os.path.join(os.getcwd(), 'Dataset', 'Books2.csv')
df = pd.read_csv(data_path)  # Replace with actual dataset path
df = df.drop("Unnamed: 0" , axis = 1)

@tool
def get_low_price_books(n: int = 5) -> List[Dict]:
    """
    Returns a list of the lowest-priced books available in the bookstore.
    
    Args:
        n (int): Number of books to return.
    
    Returns:
        List[Dict]: A list of dictionaries containing book details.
    """
    return df.nsmallest(n, "price")[['Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher',
                                     'Image-URL-L', 'price', 'discount_percentage', 'price_after_discount']
                                    ].to_dict(orient="records")

@tool
def get_high_price_books(n: int = 5) -> List[Dict]:
    """
    Returns a list of the highest-priced books available in the bookstore.
    
    Args:
        n (int): Number of books to return.
    
    Returns:
        List[Dict]: A list of dictionaries containing book details.
    """
    return df.nlargest(n, "price")[['Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher',
                                    'Image-URL-L', 'price', 'discount_percentage', 'price_after_discount']
                                   ].to_dict(orient="records")

@tool
def get_most_discounted_books(n: int = 5) -> List[Dict]:
    """
    Returns a list of books with the highest discount percentages.
    
    Args:
        n (int): Number of books to return.
    
    Returns:
        List[Dict]: A list of dictionaries containing book details.
    """
    return df.nlargest(n, "discount_percentage")[['Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher',
                                                  'Image-URL-L', 'price', 'discount_percentage', 'price_after_discount']
                                                 ].to_dict(orient="records")


# Tools for the Data Agent
@tool
def search_books_by_title(query: str) -> List[Dict]:
    """Search for books by title"""
    results = df[df['Book-Title'].str.contains(query, case=False)]
    return results.to_dict('records')

@tool
def search_books_by_author(author: str) -> List[Dict]:
    """Search for books by author"""
    results = df[df['Book-Author'].str.contains(author, case=False)]
    return results.to_dict('records')

@tool
def get_book_details(title: str) -> Optional[Dict]:
    """Get full details about a specific book"""
    book = df[df['Book-Title'].str.contains(title, case=False)].to_dict('records')
    if book:
        return book[0]
    return None

@tool
def no_book_needed():
    """Indicate that no book data is needed for the query"""
    return None