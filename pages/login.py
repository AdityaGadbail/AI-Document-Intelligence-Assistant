import streamlit as st

from authentication.session_manager import SessionManager
from database.database import SessionLocal
from services.auth_service import AuthService

st.set_page_config(page_title="Login", page_icon="📚")

CUSTOM_CSS = """
<style>
    .block-container {
        max-width: 480px;
        padding-top: 4rem;
    }
    .form-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .form-subtitle {
        text-align: center;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    div.stButton > button {
        width: 100%;
        padding: 0.6rem 0;
        border-radius: 8px;
        font-weight: 600;
        margin-top: 0.5rem;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown(
    '<div class="form-title">Welcome Back</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="form-subtitle">Login to continue</div>',
    unsafe_allow_html=True
)

with st.form("login_form"):

    email = st.text_input(
        "Email",
        placeholder="you@example.com"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    submitted = st.form_submit_button(
        "Login",
        use_container_width=True
    )

if submitted:

    email = email.strip().lower()

    if not email or not password:

        st.error("Please fill in all fields.")

    else:

        db = SessionLocal()

        try:

            user = AuthService.login_user(
                db,
                email,
                password
            )

            if user:

                SessionManager.login(user)

                st.success("Login successful!")

                st.switch_page("pages/dashboard.py")

            else:

                st.error("Invalid email or password.")

        finally:

            db.close()

st.divider()

_, center, _ = st.columns([1, 2, 1])

with center:

    if st.button(
        "Create New Account",
        use_container_width=True
    ):
        st.switch_page("pages/signup.py")