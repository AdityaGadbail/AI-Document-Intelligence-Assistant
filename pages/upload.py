import streamlit as st

from authentication.session_manager import SessionManager
from database.database import SessionLocal
from repositories.user_repository import UserRepository
from services.document_service import DocumentService
from utils.auth_guard import require_login

require_login()

st.set_page_config(
    page_title="Upload Document",
    layout="wide"
)

db = SessionLocal()

user = UserRepository.get_user_by_id(db,SessionManager.get_current_user_id())

UPLOAD_CSS = """
<style>

.main .block-container{
    max-width:900px;
    padding-top:2rem;
}

.upload-box{
    border:2px dashed #d1d5db;
    border-radius:16px;
    padding:35px;
    text-align:center;
    background:#fafafa;
}

.file-info{
    padding:15px;
    border-radius:12px;
    background:#f9fafb;
    border:1px solid #e5e7eb;
}

</style>
"""

st.markdown(UPLOAD_CSS, unsafe_allow_html=True)

col1, col2 = st.columns([6,1])

with col1:
    st.title("Upload Document")
    st.caption("Upload PDF documents for AI-powered analysis.")

with col2:
    st.write("")
    st.write("")
    if st.button("← Dashboard"):
        st.switch_page("pages/dashboard.py")

st.divider()

st.markdown(
    """
<div class="upload-box">

<h3>Drag & Drop your PDF here</h3>

<p>or browse your files</p>

</div>
""",
unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose PDF",
    type=["pdf"],
    label_visibility="collapsed"
)


if uploaded_file:
    size_mb = uploaded_file.size / (1024 * 1024)

    st.markdown(
        f"""
<div class="file-info">

<b>Filename</b><br>
{uploaded_file.name}

<br><br>

<b>Size</b><br>
{size_mb:.2f} MB

</div>
""",
unsafe_allow_html=True
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

            st.success("Document uploaded successfully! 🎉")

            st.info(
                f"""
            Filename: {document.original_filename}

            Status: {document.embedding_status}

            Document ID: {document.id}""")

        except ValueError as e:

            st.error(str(e))

        except Exception as e:
           st.exception(e)

db.close()
