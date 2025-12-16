import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# OPENAI_API_KEY
TITLE = os.getenv("TITLE")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
MODEL = os.getenv("MODEL")
PASSWORD = os.getenv("PASSWORD")

client = OpenAI()

st.title(TITLE)


def check_password():
    """Returns True if the user has entered the correct password."""

    # Check if already authenticated
    if st.session_state.get("password_correct", False):
        return True

    # Show password input
    st.title("🔒 Login")
    password = st.text_input("Enter password:", type="password", key="password_input")

    if st.button("Login"):
        # Replace "your_password" with your actual password
        if password == PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Incorrect password")

    return False


# Check password before showing the app
if not check_password():
    st.stop()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": SYSTEM_PROMPT})

for i, message in enumerate(st.session_state.messages):
    if i == 0:  # Skip first message
        continue
    if message["role"] != "system":  # Skip system messages
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Co słychać?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
