import streamlit as st
import requests

# Title
st.set_page_config(page_title="🛍️ E-commerce Chatbot", layout="centered")
st.markdown("<h2 style='text-align: center;'>🤖 Ask Our AI Support</h2>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
query = st.chat_input("Ask about your order, refund, delivery...")

if query:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Call your deployed FastAPI bot
    try:
        res = requests.post(
            "https://ecommerce-chatbot-r38v.onrender.com/chat",
            json={"query": query},
            timeout=15,
        )
        if res.status_code == 200:
            answer = res.json()["response"]
        else:
            answer = "⚠️ Bot is not responding right now."
    except Exception as e:
        answer = f"❌ Error: {str(e)}"

    # Add bot reply to history
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
