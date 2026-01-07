import streamlit as st

st.title("Career Mentor Chatbot")
st.write("Welcome to the Career Mentor Chatbot! Ask me anything about career advice.", )

user_input = st.text_input("What you want to ask: ", "")
if st.button("Send"):
    if user_input:
        import requests

        response = requests.post(
            "https://agentic-career-mentor-backend.onrender.com/chat",
            json={"message": user_input}
        )
        if response.status_code == 200:
            reply = response.json().get("reply")
            st.text_area("Mentor:", value=reply, height=500)
        else:
            st.error("Error: Could not get a response from the server.")

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

