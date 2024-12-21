from io import BytesIO
from audiorecorder import audiorecorder
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.title("Speech-to-Text Application")
st.write("Convert your voice to text using OpenAI Whisper API!")


def post_transcribe(audio) :
    with st.spinner("Transcribing..."):
        response = requests.post(f"{BACKEND_URL}/transcribe/", files={"file": ("recorded_audio.wav", audio, "audio/wav")})
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
