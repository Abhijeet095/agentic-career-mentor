import streamlit as st
import requests

st.title("Career Mentor Chatbot")
st.write("Welcome to the Career Mentor Chatbot! Ask me anything about career advice.")

# ✅ 1. Initialize session state FIRST
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ 2. Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ✅ 3. Mode selector
mode = st.radio(
    "Choose Mode",
    ["Chat with Mentor", "Get Career Plan (Agent)"]
)

# Backend URLs
CHAT_URL = "https://agentic-career-mentor.onrender.com/chat"
PLAN_URL = "https://agentic-career-mentor.onrender.com/plan"

# ✅ 4. Chat input (NO button needed)
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
