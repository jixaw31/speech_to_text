from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydub import AudioSegment
from openai import OpenAI
from io import BytesIO
from fastapi import FastAPI, HTTPException
import os
from pydantic import BaseModel
from chat import graph


# to locate and load .env file any where in the directory
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

# ----------------- Chat Endpoint -----------------


# Define the API request and response models
class ChatRequest(BaseModel):
    user_message: str

class ChatResponse(BaseModel):
    bot_reply: str

def stream_graph_updates(user_input: ChatRequest):
    config = {"configurable": {"thread_id": "1"}}
    for event in graph.stream({"messages": [("user", user_input)]}, config):
        for value in event.values():
            return value["messages"][-1].content

# print(stream_graph_updates('hello'))

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        if request.user_message:
        
            return ChatResponse(bot_reply=stream_graph_updates(request.user_message))
        else:
            return "no input"
        # return ChatResponse(bot_reply='its not working :(')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

