# Backend: FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

# Initialize FastAPI app
app = FastAPI()

# Define the API request and response models
class ChatRequest(BaseModel):
    user_message: str

class ChatResponse(BaseModel):
    bot_reply: str

# OpenAI API key (replace with your key or use env variable)
openai.api_key = "your-openai-api-key"

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Replace with your preferred model
            messages=[
                {"role": "system", "content": "You are a helpful chatbot."},
                {"role": "user", "content": request.user_message}
            ]
        )
        bot_reply = response["choices"][0]["message"]["content"]
        return ChatResponse(bot_reply=bot_reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Frontend: Streamlit
# Save this part in a separate file, e.g., `streamlit_app.py`
import streamlit as st
import requests

# API endpoint
API_URL = "http://localhost:8000/chat"

st.title("Chatbot with Streamlit and FastAPI")
st.write("Interact with your AI-powered chatbot below.")

# User input
user_message = st.text_input("You:", placeholder="Type your message here...")

if st.button("Send"):
    if user_message.strip():
        try:
            # Send user message to FastAPI backend
            response = requests.post(API_URL, json={"user_message": user_message})
            if response.status_code == 200:
                bot_reply = response.json()["bot_reply"]
                st.text_area("Bot:", value=bot_reply, height=200)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to the backend: {e}")
    else:
        st.warning("Please enter a message before sending.")

# Run FastAPI backend with: uvicorn main:app --reload
# Run Streamlit frontend with: streamlit run streamlit_app.py
