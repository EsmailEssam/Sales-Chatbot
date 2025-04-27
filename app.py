import streamlit as st
import os
import speech_recognition as sr
import functools
from modules.log_manager.log_manager import get_logger
from main import get_answer


# Initialize logger
logger = get_logger(__name__)



def recognize_speech():
    logger.info("Starting speech recognition")
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logger.debug("Listening for audio input")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language="ar-EG")
                logger.info("Successfully recognized speech")
                return text
            except sr.UnknownValueError as e:
                logger.warning("Could not understand audio")
                return "Could not understand audio"
            except sr.RequestError as e:
                logger.error(f"Could not request results from speech recognition service: {str(e)}")
                return "Speech recognition service error"
    except Exception as e:
        logger.error(f"Error in speech recognition: {str(e)}")
        return f"Error: {str(e)}"

# Configure page
st.set_page_config(page_title="Sales Chatbot", page_icon="🏷")

if 'messages' not in st.session_state:
    st.session_state.messages = []
    logger.info("Initialized new chat session")

chat_container = st.container(height=1050, border=True)

# Display chat history
for message in st.session_state.messages:
    logger.debug(f"Displaying message from {message['role']}")
    with chat_container:
        with st.chat_message(message["role"]):
            try:
                if message["role"] == "assistant":
                    respond = message["content"]
                    personalized_sales_assistance = respond.get('assistance_respond', None)
                    st.markdown(personalized_sales_assistance)
                else:
                    st.markdown(message["content"])
            except Exception as e:
                logger.error(f"Error displaying message: {str(e)}")
                st.error("Error displaying message")

# Get user input
col1, col2 = st.columns([9, 1], vertical_alignment="top")
with col1:
    user_input = st.chat_input("What is your question?", key="input")
with col2:
    if st.button("🎙"):
        user_input = recognize_speech()

if user_input:
    logger.info(f"Received user input: {user_input}")
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with chat_container:
        with st.chat_message("user"):
            st.markdown(user_input)
    
        # Get AI response
        with st.chat_message("assistant"):
            try:
                with st.spinner("Thinking..."):
                    respond = get_answer(user_input)
                    logger.debug("Received response from AI")
                    
                    filterd_list = respond['messages'][-4:]
                    logger.debug(f"Response length: {len(respond['messages'])}")
                    
                    personalized_sales_assistance = filterd_list[-1].content
                    
                    try:
                        book_recommendations = eval(filterd_list[2].content)
                        logger.debug("Successfully parsed book recommendations")
                    except Exception as e:
                        logger.warning(f"Could not parse book recommendations: {str(e)}")
                        book_recommendations = None
                    
                    st.markdown(personalized_sales_assistance)
                    
                        
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": {
                        "assistance_respond": personalized_sales_assistance, 
                    }
                })
                logger.info("Successfully processed and displayed AI response")
                
            except Exception as e:
                logger.error(f"Error processing AI response: {str(e)}")
                st.error("An error occurred while processing your request. Please try again.")