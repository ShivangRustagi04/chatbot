import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create the model object
model = genai.GenerativeModel(model_name="gemini-1.5-pro")  # use gemini-1.5-pro for stability

def clean_response(text):
    return re.sub(r"\*\*(.*?)\*\*", r"\1", text)

def generate_response(user_input):
    role_instruction = (
        "You are a medical chatbot. Your purpose is to provide medical advice, "
        "answer health-related questions, and help users understand their symptoms. "
        "If the user asks non-medical questions, politely decline."
    )
    response = model.generate_content(f"{role_instruction}\n\nUser: {user_input}\nChatbot:")
    return clean_response(response.text.strip())

def main():
    st.title("🩺 Medical Chatbot")

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    user_input = st.text_input("You:")

    if st.button("Send") and user_input.strip():
        st.session_state.conversation.append(f"You: {user_input}")
        answer = generate_response(user_input)
        st.session_state.conversation.append(f"Chatbot: {answer}")

    st.text_area(
        "Conversation",
        value="\n".join(st.session_state.conversation),
        height=400,
        disabled=True
    )

if __name__ == "__main__":
    main()
