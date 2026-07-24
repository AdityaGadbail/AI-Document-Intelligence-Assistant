import streamlit as st

from utils.auth_guard import require_login
from database.database import SessionLocal
from authentication.session_manager import SessionManager
from repositories.user_repository import UserRepository
from services.document_service import DocumentService

require_login()

st.set_page_config(
    page_title="My Documents",
    layout="wide",
    initial_sidebar_state="collapsed",
)

db = SessionLocal()

user = UserRepository.get_user_by_id(db, SessionManager.get_current_user_id())

documents = DocumentService.get_user_documents(db=db, user_id=user.id)

DOCS_CSS = """
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
        --red: #D64545;
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: var(--paper); }

    /* Hide sidebar + its toggle on this page */
    section[data-testid="stSidebar"] { display: none; }
    button[data-testid="stSidebarCollapsedControl"] { display: none; }

    .main .block-container { max-width: 900px; padding-top: 2.2rem; }

    /* ---- Page header ---------------------------------------------- */
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

    /* ---- Search input ---------------------------------------------- */
    div[data-testid="stTextInput"] input {
        border-radius: 10px;
        border: 1px solid var(--border);
        background: var(--surface);
        padding: 0.5rem 0.8rem;
        color: var(--ink);
        -webkit-text-fill-color: var(--ink);
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: var(--cobalt);
        box-shadow: 0 0 0 1px var(--cobalt);
    }

    /* ---- Document card --------------------------------------------
       Scoped to a unique key per document (doc_card_<id>) so the
       border/shadow only applies to the outer card, not the inner
       columns or button wrappers that Streamlit also renders as
       vertical blocks. */
    div[class*="st-key-doc_card_"] {
        border-radius: 14px !important;
        border: 1px solid var(--border) !important;
        background: var(--surface) !important;
        box-shadow: 0 2px 8px rgba(20, 24, 31, 0.05);
        padding: 1.2rem 1.4rem !important;
    }
    /* Safety net: neutralize borders on any other bordered wrapper Streamlit
       renders on this page (e.g. columns), so only the document card itself
       is ever boxed. */
    div[data-testid="stVerticalBlockBorderWrapper"]:not([class*="st-key-doc_card_"]) {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    .doc-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--ink);
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 0.6rem;
    }
    .doc-name .mark {
        width: 30px; height: 30px;
        border-radius: 8px;
        background: var(--cobalt-soft);
        color: var(--cobalt);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
        flex-shrink: 0;
    }
    .doc-meta-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2px 24px;
        margin-bottom: 0.8rem;
    }
    .doc-meta-row { display: flex; align-items: center; gap: 8px; color: var(--slate); font-size: 0.88rem; padding: 3px 0; }
    .doc-meta-row i { color: var(--cobalt); width: 14px; }
    .status-pill {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 2px 10px;
        border-radius: 20px;
        background: var(--cobalt-soft);
        color: var(--cobalt);
        text-transform: capitalize;
    }

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

    /* Chat button — dark fill, cobalt hover (primary action per card)
       Keys are per-document (chat_wrap_<id>), so match on a class prefix. */
    div[class*="st-key-chat_wrap_"] button {
        background: #14181F;
        color: #FFFFFF;
        border: 1px solid #14181F;
    }
    div[class*="st-key-chat_wrap_"] button:hover {
        background: var(--cobalt);
        border-color: var(--cobalt);
        color: #FFFFFF;
    }
    div[class*="st-key-chat_wrap_"] button p { color: #FFFFFF; }

    /* Delete button — subtle red outline (also per-document keys) */
    div[class*="st-key-delete_wrap_"] button {
        background: var(--surface);
        color: var(--red);
        border: 1px solid var(--border);
    }
    div[class*="st-key-delete_wrap_"] button:hover {
        background: #FCEDEC;
        border-color: var(--red);
        color: var(--red);
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


    .delete-confirmation {
    background: #FCEDEC;
    color: #B42318;
    border: 1px solid #F97066;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 12px 0;
    text-align: center;
}

.delete-confirmation .title {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 4px;
}

.delete-confirmation .subtitle {
    font-size: 13px;
    color: #7A271A;
    font-weight: 400;
}
</style>
"""

st.markdown(DOCS_CSS, unsafe_allow_html=True)

st.markdown(
    """
    <div class="page-title"><span class="mark"><i class="fa-solid fa-folder-open"></i></span> My Documents</div>
    <p class="page-subtitle">Browse, search, and manage everything you've uploaded.</p>
    """,
    unsafe_allow_html=True,
)

st.write("")

search = st.text_input(
    "Search Documents",
    placeholder="Search by filename...",
    label_visibility="collapsed",
)

if search:
    documents = [
        document for document in documents
        if search.lower() in document.original_filename.lower()
    ]

if not documents:
    st.info("No documents found.")
    st.stop()

st.write("")

for document in documents:
    with st.container(border=True, key=f"doc_card_{document.id}"):

        st.markdown(
            f"""
            <div class="doc-name">
                <span class="mark"><i class="fa-solid fa-file-lines"></i></span>
                {document.original_filename}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="doc-meta-grid">
                <div class="doc-meta-row"><i class="fa-solid fa-circle-nodes"></i>
                    Status: <span class="status-pill">{document.embedding_status.value}</span></div>
                <div class="doc-meta-row"><i class="fa-solid fa-file-lines"></i>
                    Pages: {document.page_count}</div>
                <div class="doc-meta-row"><i class="fa-solid fa-align-left"></i>
                    Words: {document.word_count}</div>
                <div class="doc-meta-row"><i class="fa-solid fa-calendar"></i>
                    {document.upload_date.strftime("%d %b %Y")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")
        chat_col, delete_col = st.columns(2)

        with chat_col:
            with st.container(key=f"chat_wrap_{document.id}"):
                if st.button("Chat", key=f"chat_{document.id}", use_container_width=True):
                    st.session_state.document_id = document.id
                    st.switch_page("pages/chat.py")

        with delete_col:
            with st.container(key=f"delete_wrap_{document.id}"):
                if st.button("Delete", key=f"delete_{document.id}", use_container_width=True):
                    st.session_state.confirm_delete = document.id
        if "confirm_delete" in st.session_state:
            st.markdown("""<div class="delete-confirmation">
            <div class="title">
            Are you sure you want to delete this document?
            </div>
            <div class="subtitle">
            This action is permanent and cannot be undone.
            </div>
            </div>""",unsafe_allow_html=True,)
            
            col1, col2 = st.columns(2)
            
            with col1:
                    if st.button(
                        "Yes, Delete",
                        use_container_width=True
                    ):
                        DocumentService.delete_document(
                            db=db,
                            document_id=st.session_state.confirm_delete,
                            user_id=user.id
                        )
            
                        del st.session_state.confirm_delete
                        st.rerun()
            
            with col2:
                    if st.button(
                        "Cancel",
                        use_container_width=True
                    ):
                        del st.session_state.confirm_delete
                        st.rerun()
                                             
st.divider()

with st.container(key="back_wrap"):
    if st.button("← Dashboard"):
        st.switch_page("pages/dashboard.py")

db.close()