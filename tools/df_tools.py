
from typing import List, Dict , Optional
from langchain_core.tools import tool 
import pandas as pd

from langchain_community.utilities import  WikipediaAPIWrapper
from langchain_community.tools import  WikipediaQueryRun


# Load book dataset
df = pd.read_csv(r"D:\Electro Pi\Sales-Chatbot\Dataset\Books2.csv")  # Replace with actual dataset path
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
def get_unique_book_titles():
    """
    Retrieves a list of unique book titles from the dataset.#+

    This function extracts all unique book titles from the 'Book-Title' column#+
    of the global DataFrame 'df'.

    Returns:
        list: A list containing all unique book titles found in the dataset.#+
    """
    return list(df['Book-Title'].unique())



@tool
def get_unique_author_names():
    """
    Retrieves a list of unique author names from the dataset.

    This function extracts all unique book titles from the 'Book-Author' column
    of the global DataFrame 'df'.

    Returns:
        list: A list containing all unique Book-Author found in the dataset.
    """
    return list(df['Book-Author'].unique())


Wikipedia_wrapper = WikipediaAPIWrapper(top_k_results= 1 , doc_content_chars_max= 300 )

Wikipedia_tool = WikipediaQueryRun(api_wrapper =  Wikipedia_wrapper)

tools =  [
        get_low_price_books , 
        get_high_price_books,
        get_most_discounted_books,
        search_books_by_title,
        search_books_by_author ,
        get_unique_book_titles,
        get_unique_author_names  ,
        Wikipedia_tool
    ]