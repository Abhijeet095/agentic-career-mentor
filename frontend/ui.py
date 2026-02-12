import streamlit as st
import requests

st.title("Career Mentor Chatbot")
st.write("Welcome to the Career Mentor Chatbot! Ask me anything about career advice.")

#  1. Initialize session state FIRST
if "messages" not in st.session_state:
    st.session_state.messages = []

#  2. Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#  3. Mode selector
mode = st.radio(
    "Choose Mode",
    ["Chat with Mentor", "Get Career Plan (Agent)"]
)

# Backend URLs
CHAT_URL = "https://agentic-career-mentor.onrender.com/chat"
PLAN_URL = "https://agentic-career-mentor.onrender.com/plan"

#  4. Chat input (NO button needed)
user_input = st.chat_input("Ask your question or enter your goal...")

if user_input:
    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        if mode == "Chat with Mentor":
            url = CHAT_URL
            payload = {"message": user_input}
        else:
            url = PLAN_URL
            payload = {"goal": user_input}

        with st.spinner("Thinking..."):
            response = requests.post(url, json=payload, timeout=60)

        if response.status_code == 200:
            reply = (
                response.json().get("reply")
                if mode == "Chat with Mentor"
                else response.json().get("plan")
            )

            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )

            with st.chat_message("assistant"):
                st.markdown(reply)
        else:
            st.error(f"Backend error: {response.status_code}")

    except Exception as e:
        st.error("Could not connect to backend.")
        st.write(e)

# Sidebar
add_selectbox = st.sidebar.selectbox(
    "Choose Option",
    ("About", "Contact")
)

if add_selectbox == "About":
    st.sidebar.title("About")
    st.sidebar.info(
        "This Career Mentor Chatbot provides guidance on career development, "
        "job searching, interview tips, and placement preparation."
    )

elif add_selectbox == "Contact":
    st.sidebar.title("Contact")
    st.sidebar.info("Contact: help@careermentor.com")

TASKS_URL = "https://agentic-career-mentor.onrender.com/tasks"

if st.sidebar.button("🗑 Clear All Tasks"):
    try:
        response = requests.delete(TASKS_URL, timeout=30)
        st.sidebar.write("Status Code:", response.status_code)
        st.sidebar.write("Response:", response.text)

        if response.status_code == 200:
            st.sidebar.success("All tasks cleared!")
            st.rerun()
        else:
            st.sidebar.error("Failed to clear tasks")

    except Exception as e:
        st.sidebar.error("Could not clear tasks")
        st.sidebar.write(e)

# if st.sidebar.button("🗑 Clear All Tasks"):
#     try:
#         requests.delete(TASKS_URL, timeout=30)
#         st.sidebar.success("All tasks cleared!")
#         st.rerun()
#     except Exception as e:
#         st.sidebar.error("Could not clear tasks")
#         st.sidebar.write(e)


# task section
st.sidebar.title("📋 Tasks")

TASKS_URL = "https://agentic-career-mentor.onrender.com/tasks"

try:
    task_response = requests.get(TASKS_URL, timeout=30)
    tasks = task_response.json().get("tasks", [])

    if not tasks:
        st.sidebar.info("No tasks yet.")
    else:
        for task in tasks:
            checkbox_key = f"task_{task['id']}"

            checked = task["status"] == "done"

            if st.sidebar.checkbox(
                task["task"],
                value=checked,
                key=checkbox_key
            ):
                if task["status"] != "done":
                    requests.post(
                        f"{TASKS_URL}/{task['id']}/done",
                        timeout=30
                    )
                    st.sidebar.success("Task marked as done!")

except Exception as e:
    st.sidebar.error("Could not load tasks")
