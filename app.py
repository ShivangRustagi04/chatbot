import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create the model object
model = genai.GenerativeModel(model_name="gemini-2.5-pro")  # use gemini-1.5-pro for stability

def clean_response(text):
    return re.sub(r"\*\*(.*?)\*\*", r"\1", text)

def generate_response(user_input):
    role_instruction = (
        "You are a medical chatbot. Your purpose is to provide medical advice, "
        "answer health-related questions, and help users understand their symptoms. "
        "If the user asks non-medical questions, politely decline."
    )

    try:
        response = model.generate_content(f"{role_instruction}\n\nUser: {user_input}\nChatbot:")

        # Safely get text
        if hasattr(response, "text") and response.text:
            output_text = response.text.strip()
        elif response.candidates and response.candidates[0].content.parts:
            output_text = response.candidates[0].content.parts[0].text.strip()
        else:
            output_text = "I'm sorry, I couldn't generate a response."

        return clean_response(output_text)

    except Exception as e:
        return f"Error: {str(e)}"


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


