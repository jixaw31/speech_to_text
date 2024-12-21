from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydub import AudioSegment
from openai import OpenAI
from io import BytesIO
import os

# to locate and load .env file any where in the directory
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------- Audio File Upload Endpoint -----------------
@app.post("/transcribe/")
async def audio_transcription(file: UploadFile = File(...)):
    converted_audio = "converted_audio.wav"
    try:
        file_content = await file.read()
        audio_data = BytesIO(file_content)
        audio = AudioSegment.from_file(audio_data)
        audio.export(converted_audio, format="wav")

        with open(converted_audio, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

        return JSONResponse(content={"transcription": transcription.text})
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        os.remove(converted_audio)

# ----------------- Root Endpoint -----------------
@app.get("/")
def root():
    return {"message": "Welcome to the Speech-to-Text API!"}
