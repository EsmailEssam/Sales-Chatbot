from crewai import Agent, Task
from config import basic_llm

final_answer_agent = Agent(
  role= "Final Answer Agent",
  goal= "To answer the user's question",
  backstory= "I am the final answer agent, I am responsible for answering the user's question",
  llm= basic_llm,
  )

final_answer_task = Task(
  description= "Answer the user's question: {user_input}",
  expected_output= "The answer to the user's question",
  agent= final_answer_agent,
)