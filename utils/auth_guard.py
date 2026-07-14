import streamlit as st
from authentication.session_manager import SessionManager

def require_login():
    if not SessionManager.is_authenticated():
        st.switch_page("app.py")
        st.stop()