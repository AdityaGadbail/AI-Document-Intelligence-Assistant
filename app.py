
import streamlit as st

from authentication.session_manager import SessionManager
from repositories.user_repository import UserRepository
from database.database import SessionLocal

st.set_page_config(
    page_title="AI Document Intelligence Assistant",
    layout="wide",
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

    /* Hide sidebar + its toggle on this entry page */
    section[data-testid="stSidebar"] { display: none; }
    button[data-testid="stSidebarCollapsedControl"] { display: none; }

    .block-container {
        max-width: 780px;
        padding-top: 4rem;
    }

    /* ---- Brand mark + heading ----------------- */
    .hero-mark {
        width: 52px; height: 52px;
        border-radius: 14px;
        background: var(--cobalt);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin: 0 auto 1.1rem auto;
    }
    .hero-title {
        text-align: center;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.4rem;
        font-weight: 700;
        color: var(--ink);
        margin-bottom: 0.25rem;
    }
    .hero-subtitle {
        text-align: center;
        color: var(--slate);
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }
    .status-badge {
        text-align: center;
        color: var(--slate);
        margin-bottom: 1.5rem;
    }
    .status-badge b { color: var(--ink); }

    /* ---- Card wrapper for the guest actions -------------------------- */
    .st-key-guest_card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.6rem 1.6rem 0.8rem 1.6rem;
        box-shadow: 0 2px 8px rgba(20, 24, 31, 0.05);
    }

    /* ---- Buttons -------------------------------------------------------- */
    div.stButton > button {
        width: 100%;
        padding: 0.6rem 0;
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid var(--border);
    }

    /* Primary (Login) — dark fill, cobalt hover */
    .st-key-login_wrap button {
        background: #14181F;
        color: #FFFFFF;
        border: 1px solid #14181F;
    }
    .st-key-login_wrap button:hover {
        background: var(--cobalt);
        border-color: var(--cobalt);
        color: #FFFFFF;
    }
    .st-key-login_wrap button p { color: #FFFFFF; }

    /* Secondary (Create Account) — cobalt outline, soft-tint hover */
    .st-key-signup_wrap button {
        background: var(--surface);
        color: var(--cobalt);
        border: 1px solid var(--cobalt);
    }
    .st-key-signup_wrap button:hover {
        background: var(--cobalt-soft);
        color: var(--cobalt);
        border-color: var(--cobalt);
    }

    /* Logout button on the authenticated view */
    .st-key-logout_wrap button {
        background: #14181F;
        color: #FFFFFF;
        border: 1px solid #14181F;
    }
    .st-key-logout_wrap button:hover {
        background: var(--cobalt);
        border-color: var(--cobalt);
        color: #FFFFFF;
    }
    .st-key-logout_wrap button p { color: #FFFFFF; }
</style>
"""


def render_header():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown('<div class="hero-mark"><i class="fa-solid fa-file-shield"></i></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">AI Document Intelligence Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Upload documents, ask questions, and get answers using RAG.</div>',
        unsafe_allow_html=True,
    )


def render_guest_view():
    st.write("")  # small spacer
    with st.container(key="guest_card"):
        col1, col2 = st.columns(2, gap="medium")

        with col1:
            with st.container(key="login_wrap"):
                if st.button("Login", use_container_width=True):
                    st.switch_page("pages/login.py")

        with col2:
            with st.container(key="signup_wrap"):
                if st.button("Create Account", use_container_width=True):
                    st.switch_page("pages/signup.py")


def main():
    render_header()

    render_guest_view()


if __name__ == "__main__":
    main()


