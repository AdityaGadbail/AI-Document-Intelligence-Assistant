import streamlit as st
from utils.auth_guard import require_login

from database.database import SessionLocal
from repositories.user_repository import UserRepository
from repositories.document_repository import DocumentRepository
from authentication.session_manager import SessionManager
from services.document_service import DocumentService
from services.ai.rag_service import RagService

from services.conversation_service import ConversationService
from services.message_service import MessageService

require_login()

st.set_page_config(
    page_title="Chat Assistant",
    layout="wide",
    initial_sidebar_state="collapsed",
)

db = SessionLocal()

user = UserRepository.get_user_by_id(db, SessionManager.get_current_user_id())


document_id = st.session_state.get("document_id")

if document_id is None:
    st.warning("No document selected.")
    st.stop()

document = DocumentRepository.get_document_by_id(db=db, document_id=document_id)

CHAT_CSS = """
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

    .main .block-container { max-width: 860px; padding-top: 2rem; padding-bottom: 6rem; }

    /* ---- Page header ---------------------------------------------- */
    .page-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--ink);
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 0.6rem 0 1.4rem 0;
    }
    .page-title .mark {
        width: 32px; height: 32px;
        border-radius: 9px;
        background: var(--cobalt);
        color: white;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.95rem;
        flex-shrink: 0;
    }

    /* "← My Documents" secondary nav button */
    .st-key-back_wrap button {
        background: var(--surface);
        color: var(--ink);
        border: 1px solid var(--border);
        border-radius: 10px;
        font-weight: 500;
    }
    .st-key-back_wrap button:hover {
        border-color: var(--cobalt);
        color: var(--cobalt);
    }

    /* ---- Chat bubbles ---------------------------------------------- */
    div[data-testid="stChatMessage"] {
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.9rem 1.1rem;
        box-shadow: 0 2px 8px rgba(20, 24, 31, 0.04);
        margin-bottom: 0.9rem;
    }
    /* Assistant bubble — plain white card */
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        background: var(--surface);
    }
    /* User bubble — soft cobalt tint so the two roles are easy to tell apart */
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: var(--cobalt-soft);
    }
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] span,
    div[data-testid="stChatMessage"] li,
    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        color: var(--ink) !important;
    }


    section[data-testid="stBottom"],
    div[data-testid="stBottomBlockContainer"] {
        background: #F7F8FA !important;
    }
    div[data-testid="stChatInput"] {
        background: var(--paper);
        border-top: 1px solid var(--border);
    }
    div[data-testid="stChatInput"] textarea,
    textarea[data-testid="stChatInputTextArea"] {
        border-radius: 10px;
        border: 1px solid var(--border) !important;
        background: var(--surface) !important;
        color: var(--ink) !important;
        -webkit-text-fill-color: var(--ink) !important;
        outline: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stChatInput"] textarea:focus,
    textarea[data-testid="stChatInputTextArea"]:focus {
        border-color: var(--cobalt) !important;
        box-shadow: 0 0 0 1px var(--cobalt) !important;
    }
    div[data-testid="stChatInput"] textarea:invalid,
    textarea[data-testid="stChatInputTextArea"]:invalid {
        border-color: var(--border) !important;
        box-shadow: none !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder,
    textarea[data-testid="stChatInputTextArea"]::placeholder {
        color: var(--slate) !important;
        opacity: 1;
    }

    /* ---- Sources expander ------------------------------------------- */
    div[data-testid="stExpander"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        background: var(--surface);
    }
    div[data-testid="stExpander"] summary {
        font-weight: 600;
        color: var(--ink);
    }
    div[data-testid="stExpander"] p,
    div[data-testid="stExpander"] span,
    div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] {
        color: var(--ink) !important;
    }
</style>
"""

st.markdown(CHAT_CSS, unsafe_allow_html=True)

with st.container(key="back_wrap"):
    if st.button("← My Documents"):
        st.switch_page("pages/my_document.py")

st.markdown(
    f'<div class="page-title"><span class="mark"><i class="fa-solid fa-file-lines"></i></span>{document.original_filename}</div>',
    unsafe_allow_html=True,
)

conversation = ConversationService.get_or_create(
    db=db, user_id=user.id, document_id=document_id, first_question="New Conversation"
)

messages = MessageService.get_history(db=db, conversation_id=conversation.id)

for message in messages:
    with st.chat_message(message.role.value):
        st.markdown(message.message)

question = st.chat_input("Ask anything about your document...")

response = None

if question:
    with st.chat_message("user"):
        st.markdown(question)

    with st.spinner("Thinking..."):
        response = RagService.ask(
            db=db,
            user_id=user.id,
            document_id=document_id,
            question=question,
        )

    with st.chat_message("assistant"):
        st.markdown(response["answer"])

if response:
    with st.expander("Sources"):
        for source in response["sources"]:
            st.markdown(source["text"])