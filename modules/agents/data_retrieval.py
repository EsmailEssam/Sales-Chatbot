from crewai import Agent, Task
from Config import llm
from modules.tools.data_retrieval_tools import get_low_price_books , get_high_price_books , get_most_discounted_books , search_books_by_title , search_books_by_author, no_book_needed
from modules.utils.retrieved_data_structure import AllExtractedBooks

data_retrieva_agent = Agent(
        role='Book Information Specialist',
        goal='To Provide accurate information about books from the database',
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
            no_book_needed
        ],
        llm = llm , 
    )

# Create the tasks
data_retrieva_task = Task(
        description='\n'.join([
                "The customer asked: '{query}'",
                "Use your tools to retrieve the relevant book information if needed."]),
        expected_output="A JSON object containing books details",
        output_json=AllExtractedBooks,
        agent=data_retrieva_agent
    )