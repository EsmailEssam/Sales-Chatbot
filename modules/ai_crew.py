from crewai import Agent, Task, Crew, Process, LLM
import os
from dotenv import load_dotenv
from crewai.tools import tool
import pandas as pd
from typing import Dict, List, Optional
from pydantic import BaseModel , Field
from config import llm

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
    return results.iloc[:3].to_dict('records')

@tool
def get_book_details(title: str) -> Optional[Dict]:
    """Get full details about a specific book"""
    book = df[df['Book-Title'].str.contains(title, case=False)].to_dict('records')
    if book:
        return book[0]
    return None


class SingleExtractedBook(BaseModel):
    Book_title: str = Field(..., title="The title of the book")
    Book_author: str = Field(..., title="The author of the book")
    Year_of_publication: str = Field(..., title="The publication year of the book")
    Publisher: str = Field(..., title="The publisher of the book")
    price: float = Field(..., title="The current price of the book")
    discount_percentage: float = Field(title="The discount percentage on the book. Set to None if no discount", default=None)
    price_after_discount: float = Field(title="The final price after applying the discount. Set to None if no discount", default=None)
    Image_URL: str = Field(title="The cover image URL of the book", default=None)

    agent_recommendation_rank: int = Field(..., title="The book's rank in the recommendation list (out of 5, Higher is Better)")
    agent_recommendation_notes: List[str] = Field(..., title="Reasons why this book is recommended or not compared to others")

class AllExtractedBooks(BaseModel):
    books: List[SingleExtractedBook]


# Create the agent
sales_agent = Agent(
    role="Professional Sales Agent",
    goal="""
    To assist users in finding the best book deals by providing recommendations based on price, discounts, and popularity.
    The agent answers in json format.
    """,
    backstory="""
    This agent is designed to help customers find the best book deals and persuade them to make a purchase.
    It analyzes book data to highlight discounts, best-value books, and premium editions.
    """,
    tools=[
        get_low_price_books , 
        get_high_price_books,
        get_most_discounted_books,
        search_books_by_title,
        search_books_by_author ,
    ],
    llm = llm , 
    verbose=True
)

data_agent = Agent(
        role='Book Information Specialist',
        goal='Provide accurate information about books from the database',
        backstory='''You are an expert on the bookstore's inventory. 
        You have access to tools that can search the database and retrieve 
        information about books, authors, prices, and availability.''',
        verbose=True,
        tools=[
            get_low_price_books , 
            get_high_price_books,
            get_most_discounted_books,
            search_books_by_title,
            search_books_by_author ,
        ],
        llm = llm , 
    )

# Create the tasks
data_task = Task(
        description='\n'.join([
                "The customer asked: '{query}'",
                "Use your tools to retrieve the relevant book information."]),
        expected_output="A JSON object containing books details",
        output_json=AllExtractedBooks,
        agent=data_agent
    )

class Consultantion(BaseModel):
    personalized_sales_assistance: str = Field(..., title="Personalized sales assistance")
    book_recommendations: AllExtractedBooks = Field(title="Book recommendations based on user preferences", default=None)

sales_consultant_agent = Agent(
        role='Book Sales Consultant',
        goal='Help customers find the perfect books and make sales',
        backstory='''You are a charismatic book lover with excellent sales skills.
        You know how to understand customer needs, recommend great books, and 
        create an engaging and personalized shopping experience. You are knowledgeable
        about literature and can suggest books based on customer preferences.''',
        verbose=True,
        llm=llm,
    )

sales_consultant_task = Task(
        description='\n'.join([
        "The customer asked: '{query}'",
        "Provide personalized book recommendations and sales assistance.",
        "Your goal is to understand their needs and help them find the perfect book.",
        "Use your knowledge of literature and sales techniques to create an engaging and helpful response."
        ]),
        expected_output="A JSON object containing personalized sales assistance and book recommendations",
        output_json=Consultantion,
        agent=sales_consultant_agent
    )

manager_agent = Agent(
        role='Bookstore Manager',
        goal='Analyze customer queries and direct them to the right specialist',
        backstory='''You are the head manager of a prestigious bookstore. 
        Your job is to analyze customer queries and determine if they need 
        specific book information or general sales assistance.''',
        verbose=True,
        llm=llm,
        allow_delegation=True
    )

manager_task = Task(
        description="""
        Analyze this customer query: '{query}'
        
        Your job is to determine if this query:
        1. Requires specific book data (like title, author, price, availability)
        2. Is a general question or needs sales assistance
        
        Respond with a clear decision and brief justification.
        If data is needed, specify what kind of data (title search, author lookup, etc.)
        """,
        expected_output="Decision on whether query needs data retrieval or sales assistance",
        agent=manager_agent
    )

ai_crew = Crew(
    agents=[
      manager_agent, data_agent, sales_consultant_agent
    ],
    tasks=[
      manager_task, data_task, sales_consultant_task
    ],
    process=Process.sequential,
    verbose=True
)