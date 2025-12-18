import logging
import os

import streamlit as st
from config import get_config
from dotenv import load_dotenv
from openai import OpenAI
from password import check_password

from shared.logger import get_logger, setup_logging

# Configure logging
setup_logging(log_file="streamlit_chat.log", log_level=logging.INFO)
logger = get_logger(__name__)

logger.info("=== Starting streamlit chat app ===")

load_dotenv()
logger.info("Line 18: Environment variables loaded")

MODEL = os.getenv("MODEL", "gpt-4o-mini")
logger.info(f"Line 20: MODEL set to {MODEL}")

domain = st.query_params.get("domain")
logger.info(f"Line 22: Query params: {dict(st.query_params)}")
logger.info(f"Line 22: Domain from query params: {domain}")
if not domain:
    # Access headers via Streamlit's experimental API
    headers = st.context.headers
    logger.info(f"Line 30: Headers: {dict(headers)}")
    domain = headers.get("X-Chat-Domain") or headers.get("x-chat-domain")
    logger.info(f"Line 35: Domain from headers params: {domain}")

config = get_config(domain)
logger.info(f"Line 24: Config retrieved: title={config.get('title')}")
client = OpenAI()
logger.info("Line 25: OpenAI client initialized")

st.title(config["title"])
logger.info("Line 27: Title displayed")

if not check_password(config["password"]):
    logger.info("Line 29: Password check failed, stopping")
    st.stop()

logger.info("Line 32: Password check passed")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = MODEL
    logger.info(f"Line 34: Initialized openai_model in session_state: {MODEL}")
else:
    logger.info(f"Line 36: openai_model already in session_state: {st.session_state['openai_model']}")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": config["system_prompt"]})
    logger.info("Line 38: Initialized messages in session_state with system prompt")
else:
    logger.info(f"Line 40: Messages already in session_state: {len(st.session_state.messages)} messages")

for i, message in enumerate(st.session_state.messages):
    if i == 0:  # Skip first message
        logger.debug(f"Line 42: Skipping first message (index {i})")
        continue
    if message["role"] != "system":  # Skip system messages
        logger.info(f"Line 44: Displaying message {i} with role {message['role']}")
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Co słychać?"):
    logger.info(f"Line 48: User prompt received: {prompt[:50]}...")
    st.session_state.messages.append({"role": "user", "content": prompt})
    logger.info(f"Line 49: User message added to session_state. Total messages: {len(st.session_state.messages)}")
    with st.chat_message("user"):
        st.markdown(prompt)
    logger.info("Line 51: User message displayed")

    with st.chat_message("assistant"):
        logger.info(f"Line 53: Creating chat completion with model {st.session_state['openai_model']}")
        logger.info(f"Line 54: Sending {len(st.session_state.messages)} messages to OpenAI")
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        logger.info("Line 59: Chat completion stream created")

        response = st.write_stream(stream)
        logger.info(f"Line 61: Response stream completed. Response length: {len(response)}")

    st.session_state.messages.append({"role": "assistant", "content": response})
    logger.info(f"Line 63: Assistant message added to session_state. Total messages: {len(st.session_state.messages)}")
else:
    logger.debug("Line 48: No user prompt received (waiting for input)")

logger.info("=== End of streamlit chat app execution ===")
