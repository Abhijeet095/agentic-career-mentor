from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import os
from typing import Dict

app = FastAPI()
client = Groq(api_key = os.getenv("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    message: str

class PlanRequest(BaseModel):
    goal: str

def planner_prompt(user_goal: str):
    return [
        {
            "role": "system",
            "content": (
                "You are a planning agent. "
                "Your job is to break a user's goal into clear, "
                "actionable steps. Output the plan in structured JSON format."
            )
        },
        {
            "role": "user",
            "content": f"Goal: {user_goal}"
        }
    ]

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

@app.post("/plan")
def plan(req: PlanRequest) -> Dict:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=planner_prompt(req.goal)
    )

    return {
        "plan": response.choices[0].message.content
    }
