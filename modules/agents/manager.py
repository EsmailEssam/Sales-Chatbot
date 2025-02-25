from crewai import Agent, Task
from Config import llm

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