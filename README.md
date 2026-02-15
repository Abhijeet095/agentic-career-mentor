# Agentic AI Career Mentor

An end-to-end Agentic AI system that generates personalized placement roadmaps, automatically extracts actionable tasks, tracks progress using persistent memory, and adapts recommendations based on user completion state.
Built using FastAPI, Streamlit, Groq (LLaMA 3.1), and SQLite, and deployed on cloud platforms.

Most placement preparation tools provide static roadmaps and generic advice. They lack:

Personalized planning
Persistent memory across sessions
Execution tracking
Adaptive recommendations

This project implements a minimal agentic AI architecture that solves these limitations through planning, memory, and task-based execution tracking.


##  Core Features
- Goal-based career roadmap generatio
- Automatic task extraction from AI-generated plans
- Persistent memory using SQLite
- Task completion tracking
- Adaptive recommendations based on progress
- Task reset functionality
- Context-aware chat responses
- Deployed backend (Render) & frontend (Streamlit Cloud)

---

##  Tech Stack
- Python
- FastAPI
- Streamlit
- Groq API (LLaMA 3.1)
- SQLite
- REST APIs
- Render
- Streamlit Cloud


## Agent Workflow
Goal → Plan → Extract Tasks → Store → Track → Adapt → Replan


# Note
This project demonstrates a production-style minimal agentic AI architecture with:

- Planning layer
- Persistent memory layer
- Execution tracking layer
- Adaptive reasoning


# Future Improvements
- Multi-user authentication system
- Reflection agent for weekly progress adjustment
- Structured JSON task extraction
- Vector-based semantic memory
