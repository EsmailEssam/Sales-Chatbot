import streamlit as st
from modules.crew import ai_crew

# Configure page
st.set_page_config(page_title="Sales Chatbot", page_icon="🏷")

def main():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Get user input
    user_input = st.chat_input("What is your question?")
    
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            result = ai_crew.kickoff(inputs={
              'user_input': user_input
              })
            
            message_placeholder.markdown(result.raw)


if __name__ == "__main__":
    main()
