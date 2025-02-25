import streamlit as st
# from modules.crew import ai_crew
from modules.process_respond import process_query, books_to_html

# Configure page
st.set_page_config(page_title="Sales Chatbot", page_icon="🏷")

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    print(message)
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            respond = message["content"]
            personalized_sales_assistance = respond.get('assistance_respond', None)
            html_book = respond.get('html_book', None)
            st.markdown(personalized_sales_assistance)
            if html_book is not None:
                st.html(html_book)
        else:
            st.markdown(message["content"])


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
        with st.spinner("Thinking..."):
            respond = process_query(user_input)
            personalized_sales_assistance = respond.get('personalized_sales_assistance', None)
            book_recommendations = respond.get('book_recommendations', None)
            st.markdown(personalized_sales_assistance)
            if book_recommendations is not None:
                html_book = books_to_html(book_recommendations)
                st.html(html_book)
            else:
                html_book = None
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": {"assistance_respond": personalized_sales_assistance, "html_book": html_book}})