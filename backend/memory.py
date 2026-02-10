import sqlite3
from datetime import datetime

DB_NAME = "agent_memory.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal TEXT,
            plan TEXT,
            created_at TEXT
        )
    """)

    #  Tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            status TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_plan(goal: str, plan: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO plans (goal, plan, created_at) VALUES (?, ?, ?)",
        (goal, plan, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()


def get_latest_plan():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT goal, plan FROM plans ORDER BY id DESC LIMIT 1"
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return {"goal": row[0], "plan": row[1]}
    return None

def add_task(task: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (task, status, created_at) VALUES (?, ?, ?)",
        (task, "pending", datetime.now().isoformat())
    )

    conn.commit()
    conn.close()


def get_tasks():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, task, status FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": r[0], "task": r[1], "status": r[2]}
        for r in rows
    ]


def complete_task(task_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status = 'done' WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()
