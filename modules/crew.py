from crewai import Crew, Process
from .agents.final_answer import final_answer_agent, final_answer_task

ai_crew = Crew(
    agents=[
        final_answer_agent
    ],
    tasks=[
        final_answer_task
    ],
    process=Process.sequential,
)