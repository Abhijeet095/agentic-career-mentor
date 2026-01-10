import streamlit as st
import requests

st.title("Career Mentor Chatbot")
st.write("Welcome to the Career Mentor Chatbot! Ask me anything about career advice.", )
BACKEND_URL = "https://agentic-career-mentor.onrender.com/chat"


mode = st.radio(
    "Choose Mode",
    ["Chat with Mentor", "Get Career Plan (Agent)"]
)


user_input = st.chat_input("Ask your question or enter your goal...")
if st.button("Send"):
   import requests

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        if mode == "Chat with Mentor":
            url = "https://agentic-career-mentor-backend.onrender.com/chat"
            payload = {"message": user_input}
        else:
            url = "https://agentic-career-mentor-backend.onrender.com/plan"
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

add_selectbox = st.sidebar.selectbox(
    "Choose Option",
    ("About", "Contact")
)
if add_selectbox == "About":
    st.sidebar.title("About")
    st.sidebar.info(
        "This Career Mentor Chatbot is designed to provide guidance and advice on career-related topics. "
        "Feel free to ask any questions you have about career development, job searching, interview tips, "
        "or any other career-related inquiries."
    )
elif add_selectbox == "Contact":
    st.sidebar.title("Contact")
    st.sidebar.info(

        "For any questions or support, please contact us at help@careermentor.com.")
    
