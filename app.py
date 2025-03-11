import streamlit as st
import os

#local Imports
from main import get_answer

import speech_recognition as sr

import os
import functools

@functools.lru_cache(maxsize=3)
def load_template(template_name):
    with open(os.path.join('template', template_name), 'r', encoding='utf-8') as f:
        return f.read()


def books_to_html(books):
    offer_card_template = load_template('offer_card_template.txt')
    norm_card_template = load_template('norm_card_template.txt')
    all_card_template = load_template('cards_template.txt')
    
    all_cards = ''
    for book in books:
        print(f"DEBUG: book = {book}, type = {type(book)}")  
        if book['discount_percentage'] > 0 or book['discount_percentage'] == "0" :
            new_card_template = offer_card_template.replace("img_url" , book['Image-URL-L'])
            new_card_template = new_card_template.replace("book_title" , book['Book-Title'])
            new_card_template = new_card_template.replace("book_author" , book['Book-Author'])
            new_card_template = new_card_template.replace("discount_percentage" , str(book['discount_percentage']))
            new_card_template = new_card_template.replace("price_befor_diccount" , str(book['price']))
            new_card_template = new_card_template.replace("price_after_discount" , str(book['price_after_discount']))
        else:
            new_card_template = norm_card_template.replace("img_url" , book['Image-URL-L'])
            new_card_template = new_card_template.replace("book_title" , book['Book-Title'])
            new_card_template = new_card_template.replace("book_author" , book['Book-Author'])
            new_card_template = new_card_template.replace("price_after_discount" , str(book['price_after_discount']))
    
        all_cards += new_card_template + '\n'
    
    new_template = all_card_template.replace('put_your_cards_here', all_cards)
    
    return new_template

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="ar-EG")
            return text
        except sr.UnknownValueError as e:
            return e
        except sr.RequestError as e:
            return e


# Configure page
st.set_page_config(page_title="Sales Chatbot", page_icon="🏷")

if 'messages' not in st.session_state:
    st.session_state.messages = []

chat_container = st.container(height=500, border=True)

# Display chat history
for message in st.session_state.messages:
    print(message)
    with chat_container:
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
col1, col2 = st.columns([9, 1], vertical_alignment="top")
with col1:
    user_input = st.chat_input("What is your question?", key="input")
with col2:
    if st.button("🎙", use_container_width=True):
        user_input = recognize_speech()


if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with chat_container:
        with st.chat_message("user"):
            st.markdown(user_input)
    
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                respond =  get_answer(user_input)
                filterd_list  =respond['messages'][-4:]
                print( "this is response length:"  , len(respond['messages']))
                personalized_sales_assistance = filterd_list[-1].content
                try:
                    book_recommendations = eval(filterd_list[2].content)
                    
                    print('this is the book recommendations results:' , book_recommendations )
                except:
                    book_recommendations = None
                    
                st.markdown(personalized_sales_assistance)
                if book_recommendations is not None:
                    html_book = books_to_html(book_recommendations)
                    st.html(html_book)
                else:
                    html_book = None
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": {"assistance_respond": personalized_sales_assistance, "html_book": html_book}})