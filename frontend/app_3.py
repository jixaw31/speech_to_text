from io import BytesIO
from audiorecorder import audiorecorder
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"
CHAT_API_URL = "http://localhost:8000/chat"

st.title("Speech-to-Text and Chatbot Application")
st.write("Convert your voice to text using OpenAI Whisper API and interact with a chatbot!")

# ----------------- Transcription Function -----------------
def post_transcribe(audio):
    with st.spinner("Transcribing..."):
        response = requests.post(
            f"{BACKEND_URL}/transcribe/",
            files={"file": ("recorded_audio.wav", audio, "audio/wav")},
        )
        if response.status_code == 200:
            result = response.json()
            st.text_area("Transcription:", result.get("transcription", ""), height=150)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

# ----------------- Chatbot Function -----------------
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

# ----------------- Real-Time Recording Transcription -----------------
st.subheader("Audio Recording Transcription")
if st.button("Record and Transcribe"):
    recorded_audio = audiorecorder()
    if len(recorded_audio) > 0:
        ra = recorded_audio.export(format="wav")
        buffer = BytesIO(ra.read())
        st.audio(buffer, format="audio/wav")
        post_transcribe(buffer)

# ----------------- Audio File Upload Transcription -----------------
st.subheader("Audio File Transcription")
uploaded_audio = st.file_uploader("Upload an audio file (e.g., .wav)")
if st.button("Upload and Transcribe") and uploaded_audio is not None:
    post_transcribe(uploaded_audio)

# ----------------- Chatbot Section -----------------
st.title("Chatbot Interaction")
st.write("Interact with your AI-powered chatbot below.")
user_message = st.text_input("You:", placeholder="Type your message here...")
if st.button("Send Message"):
    if user_message.strip():
        bot_reply = post_chat(user_message)
        if bot_reply:
            st.text_area("Bot:", value=bot_reply, height=200)
    else:
        st.warning("Please enter a message before sending.")
