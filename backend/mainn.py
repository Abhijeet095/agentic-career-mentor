from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()
client = Groq(api_key = os.getenv("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def greeting():
    return {"message": "Welcome to the Career Mentor Chatbot!"}

@app.post("/chat")
def chat(req: ChatRequest):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages = [
            {"role": "system", "content": "You are a helpful carrer mentor."},
                {"role": "user", "content": req. message}
            ]
    )
    return {
        "reply": response.choices[0].message.content
    }

