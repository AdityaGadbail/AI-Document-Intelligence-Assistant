import streamlit as st

from authentication.session_manager import SessionManager
from database.database import SessionLocal
from services.auth_service import AuthService


st.set_page_config(
    page_title="Login",
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

    /* Hide sidebar + its toggle entirely on this page */
    section[data-testid="stSidebar"] { display: none; }
    button[data-testid="stSidebarCollapsedControl"] { display: none; }

    .block-container {
        max-width: 460px;
        padding-top: 4rem;
    }

    /* ---- Brand mark + heading -------------------------------------- */
    .login-mark {
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
        margin-bottom: 1.8rem;
    }

    /* ---- Card wrapper (real container, not a broken div) ------------- */
    .st-key-login_card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.8rem 1.8rem 0.8rem 1.8rem;
        box-shadow: 0 2px 8px rgba(20, 24, 31, 0.05);
        margin-bottom: 1.2rem;
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
    /* -------- Fix Chrome / Edge Autofill -------- */

div[data-testid="stTextInput"] input:-webkit-autofill,
div[data-testid="stTextInput"] input:-webkit-autofill:hover,
div[data-testid="stTextInput"] input:-webkit-autofill:focus,
div[data-testid="stTextInput"] input:-webkit-autofill:active {

    -webkit-box-shadow: 0 0 0 1000px var(--paper) inset !important;
    -webkit-text-fill-color: var(--ink) !important;

    caret-color: var(--ink) !important;

    border: 1px solid var(--border) !important;

    transition: background-color 5000s ease-in-out 0s;
}

    /* ---- Primary (Login) button — dark fill, cobalt hover ------------- */
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

    /* ---- Secondary (Create Account) — cobalt outline, fills on hover --- */
    .st-key-create_account button {
        width: 100%;
        padding: 0.6rem 0;
        border-radius: 8px;
        font-weight: 600;
        margin-top: 0.5rem;
        background: var(--surface);
        color: var(--cobalt);
        border: 1px solid var(--cobalt);
    }
    .st-key-create_account button:hover {
        background: var(--cobalt-soft);
        color: var(--cobalt);
        border-color: var(--cobalt);
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown('<div class="login-mark"><i class="fa-solid fa-file-shield"></i></div>', unsafe_allow_html=True)



st.markdown(
    '<div class="form-title">Welcome Back</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="form-subtitle">Login to continue to AI Document Intelligence Assistant</div>',
    unsafe_allow_html=True
)

with st.container(key="login_card"):

    with st.form("login_form"):

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
            placeholder="Enter your password",
            label_visibility="collapsed",
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
    with st.container(key="create_account"):
        if st.button(
            "Create New Account",
            use_container_width=True
        ):
            st.switch_page("pages/signup.py")