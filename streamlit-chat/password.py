import logging

import streamlit as st

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("streamlit_chat.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def check_password(correct_password: str):
    """Returns True if the user has entered the correct password."""
    logger.info("Line 18: check_password function called")

    # Check if already authenticated
    if st.session_state.get("password_correct", False):
        logger.info("Line 21: User already authenticated, returning True")
        return True

    logger.info("Line 24: User not authenticated, showing login form")
    # Show password input
    st.title("🔒 Login")
    logger.info("Line 26: Login title displayed")
    password = st.text_input("Enter password:", type="password", key="password_input")
    logger.info("Line 27: Password input field displayed")

    if st.button("Login"):
        logger.info("Line 29: Login button clicked")
        # Replace "your_password" with your actual password
        if password == correct_password:
            logger.info("Line 31: Password correct, setting session state and rerunning")
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            logger.warning("Line 34: Incorrect password entered")
            st.error("❌ Incorrect password")

    logger.info("Line 37: Returning False (password not yet correct)")
    return False
