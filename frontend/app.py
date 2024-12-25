from io import BytesIO
from audiorecorder import audiorecorder
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.title("Speech-to-Text Application")
st.write("Convert your voice to text using OpenAI Whisper API!")


def post_transcribe(audio) :
    with st.spinner("Transcribing..."):
        response = requests.post(f"{BACKEND_URL}/transcribe/",
         files={"file": ("recorded_audio.wav",
         audio, "audio/wav")})
        result = response.json()
        if response.status_code == 200:
            st.text_area("Transcription:", result.get("transcription", ""), height=150)
        else:
            st.error("Error during transcription.")

# ----------------- Real-Time Recording -----------------
st.subheader("Audio Recording Transcription")
recorded_audio = audiorecorder()
if len(recorded_audio) > 0:
    ra = recorded_audio.export(format='wav')
    buffer = BytesIO(ra.read())
    st.audio(buffer)
    post_transcribe(buffer)

# ----------------- Audio File Upload -----------------
st.subheader("Audio File Transcription")
uploaded_audio = st.file_uploader("Upload an audio file (e.g., .wav)")
if uploaded_audio is not None:
    post_transcribe(uploaded_audio)


#  Chatbot ---------------------------------------------
# API endpoint
API_URL = "http://localhost:8000/chat"

st.title("Chatbot with Streamlit and FastAPI")
st.write("Interact with your AI-powered chatbot below.")

# User input

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
            st.error(f"Failed to connect to the backend.")
    else:
        st.warning("Please enter a message before sending.")

