import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


from database.database import SessionLocal
from repositories.user_repository import UserRepository
from authentication.session_manager import SessionManager
from utils.auth_guard import require_login

from services.analytics_service import AnalyticsService
from services.document_service import DocumentService

require_login()

db = SessionLocal()

user = UserRepository.get_user_by_id(db, SessionManager.get_current_user_id())
stats = AnalyticsService.get_dashboard_statistics(db=db,user_id=user.id)
documents = DocumentService.get_user_documents(db=db,user_id=user.id)
upload_activity = AnalyticsService.get_upload_activity(db,user.id)
pages = AnalyticsService.get_document_pages(db,user.id)
status = AnalyticsService.get_status_distribution(db,user.id)





st.divider()

st.subheader("Upload Activity")

if upload_activity :
    upload_df = pd.DataFrame(upload_activity,columns=["Date","Documents"])
    st.line_chart(
        upload_df.set_index("Date")
    )
else:

    st.info("No upload activity yet.")


st.divider()


st.subheader("Pages Per Document")        
if pages:

    pages_df = pd.DataFrame(
        pages,
        columns=[
            "Document",
            "Pages"
        ]
    )

    st.bar_chart(
        pages_df.set_index("Document")
    )

else:

    st.info("No documents uploaded.")

st.divider()

st.subheader("Document Status")
if status:

    labels = [s[0].value for s in status]
    values = [s[1] for s in status]

    fig, ax = plt.subplots()

    ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.axis("equal")

    st.pyplot(fig)

else:

    st.info("No document status available.")











st.title("Analytics")

st.caption(
    "View document usage, conversations and statistics."
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    col1.metric("Documents", stats["documents"])
    col2.metric("Chats", stats["conversations"])
    col3.metric("Messages", stats["messages"])
    col4.metric("Storage", f'{stats["storage"]} MB')

col1, col2 = st.columns(2)
with col1:
    st.metric(
        "Pages Processed",
        stats["pages"]
    )

    st.metric(
        "Average Pages",
        stats["average_pages"]
    )

with col2:

    st.metric(
        "Words Processed",
        f'{stats["words"]:,}'
    )

    st.metric(
        "Average Words",
        f'{stats["average_words"]:,}'
    )

st.divider()

st.subheader("Recent Documents")

if not documents:
    st.info("No uploaded documents.")

else:
    for document in documents[:5]:
        with st.container(border=True):
            st.write(f"**{document.original_filename}**")
            st.caption(f"{document.page_count} Pages • {document.word_count:,} Words")
            st.caption(document.upload_date.strftime("%d %b %Y"))


