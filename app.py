import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import time
import re

# Load environment variables from .env file
load_dotenv()

# Configure genai with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-2.5-pro')

def clean_response(response_text):
    # Remove Markdown formatting (e.g., **bold**)
    cleaned_text = re.sub(r'\*\*(.*?)\*\*', r'\1', response_text)
    return cleaned_text

def generate_response(user_input):
    # Define the role and context for the chatbot
    role_instruction = (
        "You are a medical chatbot. Your purpose is to provide medical advice, "
        "answer health-related questions, and help users understand their symptoms. "
        "If the user asks questions that are not related to medical topics, politely decline to answer."
    )
    response = model.generate_content(f"{role_instruction}\n\nUser: {user_input}\nChatbot:")
    cleaned_response = clean_response(response.text.strip())
    return cleaned_response

def main():
    st.title("Medical Chatbot using Google Generative AI")

    st.sidebar.subheader("Chat")

    # Global variable to keep track of widget keys
    widget_keys = {
        "conversation": "conversation_0",
        "user_input": "user_input_0"
    }

    if "conversation" not in st.session_state:
        st.session_state.conversation = ""

    user_input = st.text_input("You:", key=widget_keys["user_input"])

    if st.button("Send"):
        if user_input:
            st.session_state.conversation += f"\nYou: {user_input}"
            response_text = generate_response(user_input)
            st.session_state.conversation += f"\nChatbot: {response_text}"

    st.text_area("Conversation:", value=st.session_state.conversation, height=400, max_chars=None, key=widget_keys["conversation"], disabled=True)

if __name__ == "__main__":
    main()



