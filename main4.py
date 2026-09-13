import os

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Request data validate karne ke liye
class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "Gemini Chatbot API is running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=request.message
    )

    return {
        "user_message": request.message,
        "response": response.text
    }