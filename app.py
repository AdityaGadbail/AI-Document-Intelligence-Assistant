# import streamlit as st

# from authentication.session_manager import SessionManager

# st.set_page_config(
#     page_title="AI Document Intelligence Assistant",
#     page_icon="📚",
#     layout="wide"
# )


# def main():
#     st.title("AI Document Intelligence Assistant")

#     if SessionManager.is_authenticated():
#         st.success("You are logged in")

#         user_id = SessionManager.get_current_user_id()

#         st.write(f"Logged in user id :{user_id}")

#         if st.button("Logout"):
#             SessionManager.logout()
#             st.rerun()

#     else:
#         st.write("""
#         Welcome to your AI-powered document assistant.

#         Upload documents, ask questions,
#         and get answers using RAG.
#                  """)   

#         col1 , col2 = st.columns(2)

#         with col1:
#             if st.button("Login"):

#                 st.switch_page("pages/login.py")    

#         with col2:
#             if st.button("Create Account"):

#                 st.switch_page("pages/signup.py")     

# if __name__ == "__main__":
#     main()






import streamlit as st

from authentication.session_manager import SessionManager

st.set_page_config(
    page_title="AI Document Intelligence Assistant",
    page_icon="📚",
    layout="wide",
)

CUSTOM_CSS = """
<style>
    .block-container {
        max-width: 780px;
        padding-top: 4rem;
    }
    .hero-title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .hero-subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }
    .status-badge {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    div.stButton > button {
        width: 100%;
        padding: 0.6rem 0;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
"""


def render_header():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown('<div class="hero-title">AI Document Intelligence Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Upload documents, ask questions, and get answers using RAG.</div>',
        unsafe_allow_html=True,
    )


def render_authenticated_view():
    user_id = SessionManager.get_current_user_id()

    st.markdown(
        f'<div class="status-badge">Logged in as <b>{user_id}</b></div>',
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 1, 1])
    with center:
        if st.button("Logout", use_container_width=True):
            SessionManager.logout()
            st.rerun()


def render_guest_view():
    st.write("")  # small spacer
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        if st.button("Login", use_container_width=True):
            st.switch_page("pages/login.py")

    with col2:
        if st.button("Create Account", use_container_width=True):
            st.switch_page("pages/signup.py")


def main():
    render_header()

    if SessionManager.is_authenticated():
        render_authenticated_view()
    else:
        render_guest_view()


if __name__ == "__main__":
    main()
