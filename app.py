import streamlit as st

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


if __name__ == "__main__":
    main()
