from crewai import LLM
import os
from dotenv import load_dotenv
import agentops  

# Load the Key token
_ = load_dotenv(override=True)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

AGENTOPS_API_KEY = os.getenv('AGENTOPS_API_KEY')

agentops.init(
    api_key = AGENTOPS_API_KEY,
    skip_auto_end_session = True
)

llm = LLM(model='gemini/gemini-2.0-flash', api_key=GEMINI_API_KEY, temperature=0)