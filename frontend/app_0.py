import streamlit as st
import requests
from io import BytesIO
from audiorecorder import audiorecorder  # Assuming this is a custom module or library

BACKEND_URL = "http://localhost:8000"
CHAT_API_URL = f"{BACKEND_URL}/chat"

st.title("Speech-to-Text and Chatbot Application")

# ----------------- Functions -----------------
def post_transcribe(audio):
    with st.spinner("Transcribing..."):
        response = requests.post(
            f"{BACKEND_URL}/transcribe/",
            files={"file": ("recorded_audio.wav", audio, "audio/wav")}
        )
        if response.status_code == 200:
            result = response.json()
            st.text_area("Transcription:", result.get("transcription", ""), height=150)
        else:
            st.error(f"Error during transcription: {response.status_code} - {response.text}")


def post_chat(user_message):
    try:
        response = requests.post(CHAT_API_URL, json={"user_message": user_message})
        if response.status_code == 200:
            return response.json().get("bot_reply", "No reply received.")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error("Failed to connect to the backend.")
        return None

# ----------------- Real-Time Recording -----------------
st.subheader("Audio Recording Transcription")
if st.button("Record Audio"):
    recorded_audio = audiorecorder()
    if len(recorded_audio) > 0:
        ra = recorded_audio.export(format='wav')
        buffer = BytesIO(ra.read())
        st.audio(buffer)
        post_transcribe(buffer)

# ----------------- Audio File Upload -----------------
st.subheader("Audio File Transcription")
uploaded_audio = st.file_uploader("Upload an audio file (e.g., .wav)")
if uploaded_audio:
    post_transcribe(uploaded_audio)

# ----------------- Chatbot -----------------
