# import streamlit as st

# from database.database import SessionLocal 

# from services.auth_service import AuthService


# st.title("Create Account")


# username = st.text_input("Username")
# email = st.text_input("Email")
# password = st.text_input("Password")

# if st.button("Sign Up"):
#     db = SessionLocal()

#     try:
#         AuthService.register_user(db,username,email,password)

#         st.success("Account created successfully!")
#         st.info("Go to login page.")

#     except ValueError as e:
#         st.error(e)

#     finally:
#         db.close()    



import streamlit as st

from database.database import SessionLocal
from services.auth_service import AuthService

st.set_page_config(page_title="Create Account", page_icon="📚")

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

st.markdown('<div class="form-title">Create Account</div>', unsafe_allow_html=True)

with st.form("signup_form"):
    username = st.text_input("Username", placeholder="Choose a username")
    email = st.text_input("Email", placeholder="you@example.com")
    password = st.text_input("Password", type="password", placeholder="Create a password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")

    submitted = st.form_submit_button("Sign Up", use_container_width=True)

if submitted:
    if not username or not email or not password:
        st.error("Please fill in all fields.")
    elif password != confirm_password:
        st.error("Passwords do not match.")
    else:
        db = SessionLocal()
        try:
            AuthService.register_user(db, username, email, password)
            st.success("Account created successfully!")
            st.info("You can now log in with your new account.")
        except ValueError as e:
            st.error(str(e))
        finally:
            db.close()

st.divider()

_, center, _ = st.columns([1, 2, 1])
with center:
    if st.button("Already have an account? Login", use_container_width=True):
        st.switch_page("pages/login.py")