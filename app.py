import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

# Load environment variables from .env file
load_dotenv()

# Configure genai with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the model
model = genai.GenerativeModel("gemini-2.5-pro")

def clean_response(response_text):
    """Remove Markdown formatting like **bold**."""
    return re.sub(r"\*\*(.*?)\*\*", r"\1", response_text)

def generate_response(user_input):
    """Generate chatbot response using Google Generative AI."""
    role_instruction = (
        "You are a medical chatbot. Your purpose is to provide medical advice, "
        "answer health-related questions, and help users understand their symptoms. "
        "If the user asks questions that are not related to medical topics, politely decline to answer."
    )
    try:
        response = model.generate_content(f"{role_instruction}\n\nUser: {user_input}\nChatbot:")
        # Extract text safely
        if response.candidates and response.candidates[0].content.parts:
            response_text = response.candidates[0].content.parts[0].text.strip()
        else:
            response_text = "I'm sorry, I couldn't generate a response."
        return clean_response(response_text)
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("🩺 Medical Chatbot using Google Generative AI")

    # Initialize conversation history
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    user_input = st.text_input("You:")

    if st.button("Send"):
        if user_input.strip():
            # Store user message
            st.session_state.conversation.append(f"You: {user_input}")
            # Generate and store chatbot response
            response_text = generate_response(user_input)
            st.session_state.conversation.append(f"Chatbot: {response_text}")

    # Display conversation
    conversation_display = "\n".join(st.session_state.conversation)
    st.text_area("Conversation:", value=conversation_display, height=400, disabled=True)

if __name__ == "__main__":
    main()
