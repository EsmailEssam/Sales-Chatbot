from crewai import LLM
import os
from dotenv import load_dotenv

# Load the Key token
_ = load_dotenv(override=True)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

basic_llm = LLM(model='gemini/gemini-2.0-flash', api_key=GEMINI_API_KEY, temperature=0)


