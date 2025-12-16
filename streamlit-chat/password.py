import streamlit as st


def check_password(correct_password: str):
    """Returns True if the user has entered the correct password."""

    # Check if already authenticated
    if st.session_state.get("password_correct", False):
        return True

    # Show password input
    st.title("🔒 Login")
    password = st.text_input("Enter password:", type="password", key="password_input")

    if st.button("Login"):
        # Replace "your_password" with your actual password
        if password == correct_password:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Incorrect password")

    return False
