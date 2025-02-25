from crewai import Crew, Process
from .agents.manager import manager_agent , manager_task
from .agents.data_retrieval import data_retrieva_agent , data_retrieva_task
from .agents.sales_consultant import sales_consultant_agent , sales_consultant_task



ai_crew = Crew(
    agents=[
      data_retrieva_agent, sales_consultant_agent
    ],
    tasks=[
      data_retrieva_task, sales_consultant_task
    ],
    process=Process.sequential,
    verbose=True
)