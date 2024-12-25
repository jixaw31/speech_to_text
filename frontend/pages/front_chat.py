import streamlit as st
import requests

CHAT_API_URL = "http://localhost:8000/chat"

st.title("Chatbot with Streamlit and FastAPI")
st.write("Interact with your AI-powered chatbot below.")

def post_chat(user_message):
    try:
        response = requests.post(CHAT_API_URL, json={"user_message": user_message})
        if response.status_code == 200:
            return response.json().get("bot_reply", "No reply received.")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error("Failed to connect to the backend.", e)
        return None
# User input
user_message = st.text_input("You:", placeholder="Type your message here...", key="user_input")

if st.button("Send Message", key="chat_button"):
    if user_message.strip():
        bot_reply = post_chat(user_message)
        if bot_reply:
            st.text_area("Bot:", value=bot_reply, height=200)
    else:
        st.warning("Please enter a message before sending.")


