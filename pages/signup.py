import streamlit as st
import time

from database.database import SessionLocal
from authentication.session_manager import SessionManager
from services.auth_service import AuthService
import models

st.set_page_config(
    page_title="Create Account",
    initial_sidebar_state="collapsed",
)

CUSTOM_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<style>
    :root {
        --paper: #F7F8FA;
        --surface: #FFFFFF;
        --border: #E6E8EE;
        --ink: #14181F;
        --slate: #5B6472;
        --cobalt: #2F5DE3;
        --cobalt-soft: #EEF2FE;
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: var(--paper); }

    /* Hide sidebar + its toggle on this page */
    section[data-testid="stSidebar"] { display: none; }
    button[data-testid="stSidebarCollapsedControl"] { display: none; }

    .block-container {
        max-width: 980px;
        padding-top: 3.2rem;
    }

    /* ---- Brand mark + heading (page-level, spans full width) --------- */
    .signup-mark {
        width: 44px; height: 44px;
        border-radius: 12px;
        background: var(--cobalt);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        margin: 0 auto 1rem auto;
    }
    .form-title {
        text-align: center;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.9rem;
        font-weight: 700;
        color: var(--ink);
        margin-bottom: 0.25rem;
    }
    .form-subtitle {
        text-align: center;
        color: var(--slate);
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    /* ---- Card wrapper around the form -------------------------------- */
    .st-key-signup_card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.8rem 1.8rem 0.8rem 1.8rem;
        box-shadow: 0 2px 8px rgba(20, 24, 31, 0.05);
    }

    /* ---- Field labels with icons -------------------------------------- */
    .field-label {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--ink);
        margin-bottom: 0.3rem;
    }
    .field-label i { color: var(--cobalt); width: 14px; }

    /* ---- Inputs -------------------------------------------------------- */
    div[data-testid="stTextInput"] input {
        border-radius: 8px;
        border: 1px solid var(--border);
        background: var(--paper);
        padding: 0.55rem 0.75rem;
        color: var(--ink);
        caret-color: var(--ink);
        -webkit-text-fill-color: var(--ink);
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: var(--cobalt);
        box-shadow: 0 0 0 1px var(--cobalt);
        background: var(--surface);
        color: var(--ink);
        -webkit-text-fill-color: var(--ink);
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: var(--slate);
        opacity: 1;
    }

    /* ---- Primary (Sign Up) button — dark fill, cobalt hover ------------ */
    div.stFormSubmitButton > button {
        width: 100%;
        padding: 0.6rem 0;
        border-radius: 8px;
        font-weight: 600;
        margin-top: 0.5rem;
        background: #14181F;
        color: #FFFFFF;
        border: 1px solid #14181F;
    }
    div.stFormSubmitButton > button:hover {
        background: var(--cobalt);
        border-color: var(--cobalt);
        color: #FFFFFF;
    }
    div.stFormSubmitButton > button p { color: #FFFFFF; }

    /* ---- Right panel: welcome-back / login card ----------------------- */
    .st-key-side_panel {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.6rem 1.5rem;
        box-shadow: 0 2px 8px rgba(20, 24, 31, 0.05);
        height: 100%;
    }
    .side-panel-icon {
        width: 38px; height: 38px;
        border-radius: 10px;
        background: var(--cobalt-soft);
        color: var(--cobalt);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        margin-bottom: 0.9rem;
    }
    .side-panel-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--ink);
        margin-bottom: 0.3rem;
    }
    .side-panel-desc {
        color: var(--slate);
        font-size: 0.88rem;
        margin-bottom: 1.2rem;
        line-height: 1.5;
    }

    /* ---- Secondary ("Already have an account?") — cobalt outline ------ */
    .st-key-login_link button {
        width: 100%;
        padding: 0.6rem 0;
        border-radius: 8px;
        font-weight: 600;
        background: var(--surface);
        color: var(--cobalt);
        border: 1px solid var(--cobalt);
    }
    .st-key-login_link button:hover {
        background: var(--cobalt-soft);
        color: var(--cobalt);
        border-color: var(--cobalt);
    }

    /* ---- Alerts (validation / success messages) ----------------------- */
    div[data-testid="stAlert"] {
        color: #14181F !important;
        background-color: #F7F8FA !important;
        border: 1px solid #E6E8EE !important;
    }
    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] span,
    div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
        color: #14181F !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown('<div class="signup-mark"><i class="fa-solid fa-file-shield"></i></div>', unsafe_allow_html=True)
st.markdown('<div class="form-title">Create Account</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="form-subtitle">Sign up to start using AI Document Intelligence Assistant</div>',
    unsafe_allow_html=True,
)

left_col, right_col = st.columns([2, 1], gap="large")

with left_col:
    with st.container(key="signup_card"):

        with st.form("signup_form"):

            st.markdown('<div class="field-label"><i class="fa-solid fa-user"></i>Username</div>', unsafe_allow_html=True)
            username = st.text_input(
                "Username",
                placeholder="Choose a username",
                label_visibility="collapsed",
            )

            st.markdown('<div class="field-label"><i class="fa-solid fa-envelope"></i>Email</div>', unsafe_allow_html=True)
            email = st.text_input(
                "Email",
                placeholder="you@example.com",
                label_visibility="collapsed",
            )

            st.markdown('<div class="field-label"><i class="fa-solid fa-lock"></i>Password</div>', unsafe_allow_html=True)
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password",
                label_visibility="collapsed",
            )

            st.markdown('<div class="field-label"><i class="fa-solid fa-lock"></i>Confirm Password</div>', unsafe_allow_html=True)
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password",
                label_visibility="collapsed",
            )

            submitted = st.form_submit_button("Sign Up", use_container_width=True)

with right_col:
    alert_area = st.container(key="alert_panel")

    with st.container(key="side_panel"):
        st.markdown('<div class="side-panel-icon"><i class="fa-solid fa-right-to-bracket"></i></div>', unsafe_allow_html=True)
        st.markdown('<div class="side-panel-title">Already have an account?</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="side-panel-desc">Log back in to pick up where you left off with your documents and conversations.</div>',
            unsafe_allow_html=True,
        )
        with st.container(key="login_link"):
            if st.button("Login", use_container_width=True):
                st.switch_page("pages/login.py")

if submitted:
    if not username or not email or not password or not confirm_password:
        with alert_area:
            st.error("Please fill in all fields.")
    elif password != confirm_password:
        with alert_area:
            st.error("Passwords do not match.")
    else:
        username = username.strip()
        email = email.strip().lower()
        db = SessionLocal()
        try:
            with st.spinner("Creating account..."):
                new_user = AuthService.register_user(db, username, email, password)
            SessionManager.login(new_user)
            with alert_area:
                st.success("Account created successfully!")
            time.sleep(1)
            st.switch_page("pages/dashboard.py")
        except ValueError as e:
            with alert_area:
                st.error(str(e))
        except Exception:
            with alert_area:
                st.error("Something went wrong. Please try again.")
        finally:
            db.close()
