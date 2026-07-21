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
db = SessionLocal()

user = UserRepository.get_user_by_id(db, SessionManager.get_current_user_id())


document_id = st.session_state.get("document_id")

if document_id is None:
    st.warning("No document selected.")
    st.stop()

document = DocumentRepository.get_document_by_id(db=db,document_id=document_id)  

if st.button("← My Documents"):

    st.switch_page(
        "pages/my_document.py"
    )

st.title(
    f"📄 {document.original_filename}"
)

conversation = ConversationService.get_or_create(db=db,user_id=user.id,document_id=document_id,first_question="New Conversation")

messages = MessageService.get_history(db=db,conversation_id=conversation.id)

for message in messages:

    with st.chat_message(message.role.value):
        st.markdown(message.message)


question = st.chat_input("Ask anything about your document...")

# if question:
#     with st.chat_message("user"):
#         st.markdown(question)

#     with st.spinner(
#     "Thinking..."
#     ):  
#         response = RagService.ask(db=db,user_id=user.id,document_id=document_id,question=question)

#     with st.chat_message("assistant"):
#         st.markdown(response["answer"])

# with st.expander(
#     "Sources"
# ):

#     for source in response["sources"]:

#         st.markdown(
#             source["text"]
#         )    

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