from crewai import Agent, Task
from Config import llm
from modules.utils.retrieved_data_structure import Consultantion


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
        "don't recommend any book if the customer doesn't ask for any book",
        "Use your knowledge of literature and sales techniques to create an engaging and helpful response."
        ]),
        expected_output="A JSON object containing personalized sales assistance and book recommendations",
        output_json=Consultantion,
        agent=sales_consultant_agent
    )
