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

st.set_page_config(
    page_title="Analytics",
    layout="wide",
    initial_sidebar_state="collapsed",
)

db = SessionLocal()

user = UserRepository.get_user_by_id(db, SessionManager.get_current_user_id())
stats = AnalyticsService.get_dashboard_statistics(db=db, user_id=user.id)
documents = DocumentService.get_user_documents(db=db, user_id=user.id)
upload_activity = AnalyticsService.get_upload_activity(db, user.id)
pages = AnalyticsService.get_document_pages(db, user.id)
status = AnalyticsService.get_status_distribution(db, user.id)

ANALYTICS_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
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

    .main .block-container { max-width: 1100px; padding-top: 2.2rem; }

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

    .section-label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--slate);
        margin: 2rem 0 0.9rem 0;
    }

    /* ---- Metric cards ------------------------------------------------- */
    .metric-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,.05);
        height: 100%;
    }
    .metric-title { font-size: 15px; color: var(--slate); }
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 30px;
        font-weight: 700;
        margin-top: 8px;
        color: var(--ink);
    }

    /* ---- Chart cards (wrap native + matplotlib charts consistently) --- */
    div[class*="st-key-chart_card_"] {
        border-radius: 14px !important;
        border: 1px solid var(--border) !important;
        background: var(--surface) !important;
        box-shadow: 0 2px 8px rgba(20, 24, 31, 0.05);
        padding: 1.2rem 1.3rem !important;
    }
    .chart-card-title {
        font-weight: 600;
        color: var(--ink);
        font-size: 0.98rem;
        margin-bottom: 0.6rem;
    }

    /* ---- Recent document cards ----------------------------------- */
    div[class*="st-key-recent_doc_"] {
        border-radius: 14px !important;
        border: 1px solid var(--border) !important;
        background: var(--surface) !important;
        box-shadow: 0 2px 8px rgba(20, 24, 31, 0.05);
        padding: 1rem 1.2rem !important;
    }
    .doc-row { display: flex; align-items: center; gap: 12px; }
    .doc-row .mark {
        width: 30px; height: 30px;
        border-radius: 8px;
        background: var(--cobalt-soft);
        color: var(--cobalt);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
        flex-shrink: 0;
    }
    .doc-row .name { font-weight: 600; color: var(--ink); font-size: 0.95rem; }
    .doc-row .meta { color: var(--slate); font-size: 0.82rem; margin-top: 2px; }

    /* "← Dashboard" secondary nav button */
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
</style>
"""

st.markdown(ANALYTICS_CSS, unsafe_allow_html=True)

header_left, header_right = st.columns([5, 1])

with header_left:
    st.markdown(
        """
        <div class="page-title"><span class="mark"><i class="fa-solid fa-chart-line"></i></span> Analytics</div>
        <p class="page-subtitle">View document usage, conversations and statistics.</p>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    st.write("")
    with st.container(key="back_wrap"):
        if st.button("← Dashboard"):
            st.switch_page("pages/dashboard.py")

st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)

overview_cols = st.columns(4)
overview_metrics = [
    ("Documents", stats["documents"]),
    ("Chats", stats["conversations"]),
    ("Messages", stats["messages"]),
    ("Storage", f'{stats["storage"]} MB'),
]

for col, (label, value) in zip(overview_cols, overview_metrics):
    with col:
        st.markdown(
            f"""<div class="metric-card"><div class="metric-title">{label}</div>
            <div class="metric-value">{value}</div></div>""",
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-label">Document Processing</div>', unsafe_allow_html=True)

processing_cols = st.columns(4)
processing_metrics = [
    ("Pages Processed", stats["pages"]),
    ("Average Pages", stats["average_pages"]),
    ("Words Processed", f'{stats["words"]:,}'),
    ("Average Words", f'{stats["average_words"]:,}'),
]

for col, (label, value) in zip(processing_cols, processing_metrics):
    with col:
        st.markdown(
            f"""<div class="metric-card"><div class="metric-title">{label}</div>
            <div class="metric-value">{value}</div></div>""",
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-label">Trends</div>', unsafe_allow_html=True)

with st.container(key="chart_card_upload"):
    st.markdown('<div class="chart-card-title">Upload Activity</div>', unsafe_allow_html=True)
    if upload_activity:
        upload_df = pd.DataFrame(upload_activity, columns=["Date", "Documents"])
        st.line_chart(upload_df.set_index("Date"), color=["#2F5DE3"])
    else:
        st.info("No upload activity yet.")

st.write("")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    with st.container(key="chart_card_pages"):
        st.markdown('<div class="chart-card-title">Pages Per Document</div>', unsafe_allow_html=True)
        if pages:
            pages_df = pd.DataFrame(pages, columns=["Document", "Pages"])
            st.bar_chart(pages_df.set_index("Document"), color=["#2F5DE3"])
        else:
            st.info("No documents uploaded.")

with chart_col2:
    with st.container(key="chart_card_status"):
        st.markdown('<div class="chart-card-title">Document Status</div>', unsafe_allow_html=True)
        if status:
            labels = [s[0].value for s in status]
            values = [s[1] for s in status]

            palette = ["#2F5DE3", "#8AA6F2", "#14181F", "#B7C2D6", "#5B6472"]

            fig, ax = plt.subplots()
            fig.patch.set_facecolor("#FFFFFF")
            ax.set_facecolor("#FFFFFF")

            wedges, texts, autotexts = ax.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                colors=palette[: len(values)],
                textprops={"color": "#14181F"},
            )
            for autotext in autotexts:
                autotext.set_color("#FFFFFF")

            ax.axis("equal")

            st.pyplot(fig)
        else:
            st.info("No document status available.")

st.markdown('<div class="section-label">Recent Documents</div>', unsafe_allow_html=True)

if not documents:
    st.info("No uploaded documents.")
else:
    for document in documents[:5]:
        with st.container(key=f"recent_doc_{document.id}"):
            st.markdown(
                f"""
                <div class="doc-row">
                    <div class="mark"><i class="fa-solid fa-file-lines"></i></div>
                    <div>
                        <div class="name">{document.original_filename}</div>
                        <div class="meta">{document.page_count} Pages • {document.word_count:,} Words • {document.upload_date.strftime("%d %b %Y")}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

db.close()