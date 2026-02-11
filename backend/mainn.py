from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import os
from typing import Dict, Optional
from memory import init_db, save_plan, get_latest_plan
from memory import add_task, get_tasks, complete_task


init_db()

app = FastAPI()
client = Groq(api_key = os.getenv("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    message: str

class PlanRequest(BaseModel):
    goal: str

class TaskRequest(BaseModel):
    task: str

def chat_prompt(user_message: str, memory: Optional[dict], tasks: list):
    task_context = (
        "Current tasks and progress:\n" +
        "\n".join(
            f"- {t['task']} ({t['status']})"
            for t in tasks
        )
        if tasks else
        "No tasks available."
    )

    memory_context = (
        f"User goal: {memory['goal']}\nPlan:\n{memory['plan']}"
        if memory else
        "No prior plan."
    )

    return [
        {
            "role": "system",
            "content": (
                "You are a career mentor AI agent. "
                "Use the user's goal, plan, and task progress to give adaptive advice.\n\n"
                f"{memory_context}\n\n"
                f"{task_context}"
            )
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

def planner_prompt(user_goal: str):
    return [
        {
            "role": "system",
            "content": (
                "You are a planning agent.\n"
                "Create a clear career plan.\n\n"
                "IMPORTANT:\n"
                "1. First write the detailed plan in plain text.\n"
                "2. Then at the end write a section exactly like this:\n\n"
                "TASK_LIST:\n"
                "- Task 1\n"
                "- Task 2\n"
                "- Task 3\n\n"
                "Keep tasks short and actionable."
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
    memory = get_latest_plan()
    tasks = get_tasks()


    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=chat_prompt(req.message, memory, tasks)
    )

    return {
        "reply": response.choices[0].message.content
    }
    

@app.post("/plan")
def plan(req: PlanRequest):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=planner_prompt(req.goal)
    )

    plan_text = response.choices[0].message.content

    # Save plan
    save_plan(req.goal, plan_text)

    #  Extract tasks
    if "TASK_LIST:" in plan_text:
        task_section = plan_text.split("TASK_LIST:")[1]
        lines = task_section.strip().split("\n")

        for line in lines:
            if line.startswith("-"):
                task = line.replace("-", "").strip()
                if task:
                    add_task(task)

    return {
        "goal": req.goal,
        "plan": plan_text
    }



@app.get("/memory")
def get_memory():
    memory = get_latest_plan()
    if memory:
        return memory
    return {"message": "No memory found"}

@app.post("/tasks")
def create_task(req: TaskRequest):
    add_task(req.task)
    return {"message": "Task added"}

@app.get("/tasks")
def view_tasks():
    return {"tasks": get_tasks()}

@app.post("/tasks/{task_id}/done")
def mark_done(task_id: int):
    complete_task(task_id)
    return {"message": "Task marked as completed"}
