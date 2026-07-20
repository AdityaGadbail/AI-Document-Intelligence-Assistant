import streamlit as st
import textwrap

from authentication.session_manager import SessionManager
from database.database import SessionLocal
from repositories.user_repository import UserRepository
from services.document_service import DocumentService
from utils.auth_guard import require_login

require_login()

st.set_page_config(
    page_title="Upload Document",
    layout="wide",
    initial_sidebar_state="collapsed",
)

db = SessionLocal()

user = UserRepository.get_user_by_id(db, SessionManager.get_current_user_id())

UPLOAD_CSS = """
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
        --green: #1F9D6C;
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: var(--paper); }

    /* Hide sidebar + its toggle on this page */
    section[data-testid="stSidebar"] { display: none; }
    button[data-testid="stSidebarCollapsedControl"] { display: none; }

    .main .block-container {
        max-width: 900px;
        padding-top: 2.2rem;
    }

    h1 { font-family: 'Space Grotesk', sans-serif; color: var(--ink); }

    /* ---- Page header row ---------------------------------------------- */
    .page-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.9rem;
        font-weight: 700;
        color: var(--ink);
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 0;
    }
    .page-title .mark {
        width: 34px; height: 34px;
        border-radius: 9px;
        background: var(--cobalt);
        color: white;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.05rem;
    }
    .page-subtitle { color: var(--slate); font-size: 0.95rem; margin: 0.35rem 0 0 44px; }

    /* ---- Upload dropzone ------------------------------------------------ */
    .upload-box {
        border: 2px dashed var(--border);
        border-radius: 16px;
        padding: 35px;
        text-align: center;
        background: var(--surface);
    }
    .upload-box i {
        font-size: 2rem;
        color: var(--cobalt);
        margin-bottom: 0.6rem;
        display: block;
    }
    .upload-box h3 { color: var(--ink); font-family: 'Space Grotesk', sans-serif; margin: 0.4rem 0 0.2rem 0; }
    .upload-box p { color: var(--slate); margin: 0; }

    /* ---- File info card ------------------------------------------------- */
    .file-info {
        padding: 18px 20px;
        border-radius: 12px;
        background: var(--surface);
        border: 1px solid var(--border);
        box-shadow: 0 2px 8px rgba(20, 24, 31, 0.05);
    }
    .file-info .row { display: flex; align-items: center; gap: 10px; padding: 6px 0; }
    .file-info .row i { color: var(--cobalt); width: 16px; }
    .file-info b { color: var(--ink); }
    .file-info span.value { color: var(--slate); }

    /* ---- Buttons -------------------------------------------------------- */
    div.stButton > button {
        border-radius: 10px;
        border: 1px solid var(--border);
        background: var(--surface);
        color: var(--ink);
        font-weight: 500;
    }
    div.stButton > button:hover {
        border-color: var(--cobalt);
        color: var(--cobalt);
    }

    /* "← Dashboard" secondary nav button */
    .st-key-back_wrap button {
        background: var(--surface);
        color: var(--ink);
        border: 1px solid var(--border);
    }
    .st-key-back_wrap button:hover {
        border-color: var(--cobalt);
        color: var(--cobalt);
    }

    /* Primary "Upload Document" button — dark fill, cobalt hover */
    div.stButton > button[kind="primary"] {
        background: #14181F;
        color: #FFFFFF;
        border: 1px solid #14181F;
    }
    div.stButton > button[kind="primary"]:hover {
        background: var(--cobalt);
        border-color: var(--cobalt);
        color: #FFFFFF;
    }
    div.stButton > button[kind="primary"] p { color: #FFFFFF; }


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

st.markdown(UPLOAD_CSS, unsafe_allow_html=True)

col1, col2 = st.columns([6, 1])

with col1:
    st.markdown(
        """
        <div class="page-title"><span class="mark"><i class="fa-solid fa-cloud-arrow-up"></i></span> Upload Document</div>
        <p class="page-subtitle">Upload PDF documents for AI-powered analysis.</p>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.write("")
    with st.container(key="back_wrap"):
        if st.button("← Dashboard"):
            st.switch_page("pages/dashboard.py")

st.divider()

st.markdown(
    """
    <div class="upload-box">
    <i class="fa-solid fa-file-arrow-up"></i>
    <h3>Drag & Drop your PDF here</h3>
    <p>or browse your files</p>
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Choose PDF",
    type=["pdf"],
    label_visibility="collapsed"
)


if uploaded_file:
    size_mb = uploaded_file.size / (1024 * 1024)

    st.write("")
    st.markdown(
        f"""
        <div class="file-info">
            <div class="row"><i class="fa-solid fa-file-lines"></i><b>Filename:</b>&nbsp;<span class="value">{uploaded_file.name}</span></div>
            <div class="row"><i class="fa-solid fa-weight-hanging"></i><b>Size:</b>&nbsp;<span class="value">{size_mb:.2f} MB</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if uploaded_file:

    st.write("")

    if st.button(
        "Upload Document",
        use_container_width=True,
        type="primary"
    ):

        try:

            document = DocumentService.upload_document(
                db=db,
                uploaded_file=uploaded_file,
                user_id=user.id
            )

            st.success("Document uploaded successfully!")

            details = textwrap.dedent(f"""
            Filename: {document.original_filename}

            Status: {document.embedding_status}

            Document ID: {document.id}
            
            Uploaded : {document.upload_date}

            """).strip()

            st.info(details)    

        
        except ValueError as e:

            st.error(str(e))

        except Exception as e:
           st.exception(e)

db.close()