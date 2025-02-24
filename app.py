import streamlit as st
from modules.crew import ai_crew

# Configure page
st.set_page_config(page_title="Sales Chatbot", page_icon="🏷")

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    print(message)
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Get user input
user_input = st.chat_input("What is your question?")

with open(r"D:\Electro Pi\Sales-Chatbot\notebooks\ai-agent-output\sales_agent_output.html" , "r" ,  encoding="utf-8") as f:
    html_output = f.read()  # Read HTML file content
    

st.markdown(html_output, unsafe_allow_html=True)  # Render HTML in Streamlit chatbox

if user_input:
    # Add user message to chat history
    
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get AI response
    with st.chat_message("assistant"):
        result = ai_crew.kickoff(inputs={
          'user_input': user_input
          })
        
        st.markdown(result.raw)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": result.raw})