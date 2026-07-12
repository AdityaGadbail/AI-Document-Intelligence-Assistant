import streamlit as st


class SessionManager:

    @staticmethod
    def login(user):
        st.session_state["user_id"] = user.id

    @staticmethod
    def logout():
        st.session_state.clear()

    @staticmethod
    def is_authenticated():
        return "user_id" in st.session_state

    @staticmethod
    def get_current_user_id():
        return  st.session_state.get("user_id")
