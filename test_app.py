import streamlit as st
import time
from typing import Dict, Any, TypedDict, Sequence
from langchain_core.callbacks import BaseCallbackHandler
from langgraph.graph import END, StateGraph
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain_core.messages import BaseMessage

# Local importing
from tools.df_tools import tools

# Load environment variables
load_dotenv()

# Get API key from environment variables
api_key = os.getenv('GEMINI_API_KEY')

# Define the state schema
class GraphState(TypedDict):
    messages: Sequence[BaseMessage]

# Custom callback handler for streaming updates
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        # Update the container with the new text
        self.container.markdown(self.text)

def main():
    st.title("LangGraph Streaming Demo")
    
    # Create a container to display the streaming text
    chat_container = st.empty()
    
    # Initialize the stream handler with the container
    stream_handler = StreamHandler(chat_container)
    
    # Create your LangGraph workflow with streaming support
    def create_graph():
        workflow = StateGraph(GraphState)
        
        def agent_node(state: GraphState) -> Dict[str, Any]:
            messages = state["messages"]
            
            # Configure your LLM with streaming and the callback handler
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0.0,
                api_key=api_key,
                streaming=True,
                callbacks=[stream_handler]
            )
            
            # Invoke the LLM (streaming tokens will trigger the callback)
            response = llm.invoke(messages)
            
            return {
                "messages": messages + [response],
                "next": END
            }
            
        workflow.add_node("agent_node", agent_node)
        workflow.set_entry_point("agent_node")
        return workflow.compile()

    # Create the compiled graph
    graph = create_graph()
    
    # Handle user input
    user_input = st.text_input("Enter your question:")
    if user_input:
        # Initial state with the user-provided message
        state = {"messages": [{"role": "user", "content": user_input}]}
        
        try:
            with st.spinner("Generating response..."):
                # Iterate over the streaming generator.
                # The callback updates the container as tokens are received.
                for _ in graph.stream(state):
                    # A small sleep helps the UI refresh between tokens.
                    time.sleep(0.1)
                    
            # Optionally, update one last time once streaming is complete.
            chat_container.markdown(stream_handler.text)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
