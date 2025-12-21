import os

import streamlit as st
from config import get_config
from dotenv import load_dotenv
from openai import OpenAI
from password import check_password
from prompt import get_system_prompt

from shared.chat_config import ChatConfig

# Configure logging
load_dotenv()

MODEL = os.getenv("MODEL", "gpt-4o-mini")

# Access headers via Streamlit's experimental API
headers = st.context.headers
domain = headers.get("X-Chat-Domain") or headers.get("x-chat-domain")

config: ChatConfig = get_config(domain)

client = OpenAI()

st.set_page_config(page_title=config.title)
st.title(config.title)

if not check_password(config.password):
    st.stop()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = MODEL

if "messages" not in st.session_state:
    st.session_state.messages = []
    system_prompt = get_system_prompt(config)
    st.session_state.messages.append({"role": "system", "content": system_prompt})

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
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )

        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
