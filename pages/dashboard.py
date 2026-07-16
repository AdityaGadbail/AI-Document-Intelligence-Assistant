import streamlit as st

from utils.auth_guard import require_login
from database.database import SessionLocal
from authentication.session_manager import SessionManager
from repositories.user_repository import UserRepository

require_login()

db = SessionLocal()

user = UserRepository.get_user_by_id(db, SessionManager.get_current_user_id())

st.set_page_config(
    page_title="AI Document Intelligence Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# Design tokens & global styles
# ----------------------------------------------------------------------------

DASHBOARD_CSS = """
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
        --green: #1F9D6C;
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: var(--paper); }
    .main .block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1180px; }

    h1, h2, h3, .app-title { font-family: 'Space Grotesk', sans-serif; }

    /* ---- Kicker / section label -------------------------------------- */
    .kicker {
        display: flex;
        align-items: center;
        gap: 8px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--slate);
        margin: 2.2rem 0 0.9rem 0;
    }
    .kicker .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--cobalt); display: inline-block; }

    /* ---- Header -------------------------------------------------------- */
    .app-title {
        font-size: 1.9rem;
        font-weight: 700;
        color: var(--ink);
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .app-title .mark {
        width: 34px; height: 34px;
        border-radius: 9px;
        background: var(--cobalt);
        color: white;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.05rem;
    }
    .app-subtitle { color: var(--slate); font-size: 0.96rem; margin: 0.35rem 0 0 44px; }
    .header-welcome { text-align: right; color: var(--slate); font-size: 1.05rem; padding-top: 6px; }
    .header-welcome b { color: var(--ink); font-weight: 700; font-size: 1.2rem; }

    /* ---- Metric cards ---------------------------------------------- */
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
        font-size: 32px;
        font-weight: 700;
        margin-top: 8px;
        color: var(--ink);
    }

    /* ---- Action cards ------------------------------------------------- */
    .action-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 22px;
        min-height: 170px;
        box-shadow: 0 2px 8px rgba(0,0,0,.05);
    }
    .action-title { font-size: 22px; font-weight: 700; color: var(--ink); }
    .action-desc { color: var(--slate); margin-top: 10px; }


/* Default buttons (Upload / Documents / Chat / Analytics) */
    div.stButton > button {
        border-radius: 10px;
        border: 1px solid #14181F;
        background: #14181F;
        color: #FFFFFF;
        font-weight: 500;
    }
    div.stButton > button:hover {
        border-color: var(--cobalt);
        background: var(--cobalt);
        color: #FFFFFF;
    }
    div.stButton > button p {
        color: #FFFFFF;
    }

    /* Logout button only — scoped, doesn't affect other buttons */
    .st-key-logout_wrap {
        display: flex;
        justify-content: flex-end;
    }
    .st-key-logout_wrap button {
        border-radius: 8px;
        border: 1px solid #14181F;
        background: #14181F;
        color: #FFFFFF;
        font-weight: 600;
        padding: 0.35rem 1.2rem;
    }
    .st-key-logout_wrap button:hover {
        background: var(--cobalt);
        border-color: var(--cobalt);
        color: #FFFFFF;
    }
    .st-key-logout_wrap button p {
        color: #FFFFFF;
    }

    /* Icon styling inside cards */
    .app-title .mark i { color: #FFFFFF; font-size: 1rem; }
    .action-title i { color: var(--cobalt); margin-right: 8px; }




    /* ---- Activity list --------------------------------------------- */
    .activity-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.4rem 1.3rem;
        box-shadow: 0 2px 8px rgba(0,0,0,.05);
    }
    .activity-row { display: flex; align-items: center; gap: 12px; padding: 0.85rem 0; }
    .activity-row + .activity-row { border-top: 1px solid var(--border); }
    .activity-icon {
        width: 32px; height: 32px;
        border-radius: 8px;
        background: var(--cobalt-soft);
        display: flex; align-items: center; justify-content: center;
        font-size: 0.9rem;
        flex-shrink: 0;
    }
    .activity-text { flex: 1; }
    .activity-title-row { font-size: 0.9rem; color: var(--ink); font-weight: 500; }
    .activity-meta { font-size: 0.78rem; color: var(--slate); margin-top: 1px; }
    .activity-time { font-size: 0.78rem; color: var(--slate); white-space: nowrap; }
    .activity-empty { text-align: center; color: var(--slate); font-size: 0.88rem; padding: 2.2rem 0; }

    
</style>
"""

st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# 1. Header
# ----------------------------------------------------------------------------
header_left,header_right = st.columns(2)
with header_left:
    st.markdown(
        """
        <div class="app-title"><i class="fa-solid fa-file-shield"></i> AI Document Intelligence Assistant</div>
        <p class="app-subtitle">Manage your documents and chat with AI.</p>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    with st.container(key="logout_wrap"):
        if st.button("Logout", key="logout"):
            SessionManager.logout()
            st.switch_page("app.py")
    st.markdown(
        f"""
        <div class="header-welcome">
            Welcome back, <b>{user.username}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='border-bottom:1px solid #E6E8EE;margin-bottom:0.4rem;'></div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# 2. Statistics section
# ----------------------------------------------------------------------------
st.markdown('<div class="kicker"><span class="dot"></span>Overview</div>', unsafe_allow_html=True)

document_count = 0
chat_count = 0
message_count = 0
storage_used = "0 MB"

stat_cols = st.columns(4)

with stat_cols[0]:
    st.markdown(
        f"""<div class="metric-card"><div class="metric-title">Documents</div>
        <div class="metric-value">{document_count}</div></div>""",
        unsafe_allow_html=True,
    )

with stat_cols[1]:
    st.markdown(
        f"""<div class="metric-card"><div class="metric-title">Chats</div>
        <div class="metric-value">{chat_count}</div></div>""",
        unsafe_allow_html=True,
    )

with stat_cols[2]:
    st.markdown(
        f"""<div class="metric-card"><div class="metric-title">Messages</div>
        <div class="metric-value">{message_count}</div></div>""",
        unsafe_allow_html=True,
    )

with stat_cols[3]:
    st.markdown(
        f"""<div class="metric-card"><div class="metric-title">Storage</div>
        <div class="metric-value">{storage_used}</div></div>""",
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------------------
# 3. Quick actions (2x2 grid)
# ----------------------------------------------------------------------------
st.write("")
st.markdown('<div class="kicker"><span class="dot"></span>Quick Actions</div>', unsafe_allow_html=True)

row1col1, row1col2 = st.columns(2)
row2col1, row2col2 = st.columns(2)

with row1col1:
    st.markdown(
        """
        <div class="action-card">
        <div class="action-title"><i class="fa-solid fa-cloud-arrow-up"></i>Upload Documents</div>
        <div class="action-desc">Upload PDFs and prepare them for AI-powered search and chat.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Upload", use_container_width=True, key="upload"):
        st.switch_page("pages/upload.py")

with row1col2:
    st.markdown(
        """
        <div class="action-card">
        <div class="action-title"><i class="fa-solid fa-folder-open"></i>My Documents</div>
        <div class="action-desc">Browse, manage and delete uploaded documents.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Documents", use_container_width=True, key="docs"):
        st.switch_page("pages/documents.py")

with row2col1:
    st.markdown(
        """
        <div class="action-card">
<div class="action-title"><i class="fa-solid fa-comments"></i>Chat Assistant</div>
        <div class="action-desc">Ask questions and receive answers grounded in your uploaded PDFs.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Chat", use_container_width=True, key="chat"):
        st.switch_page("pages/chat.py")

with row2col2:
    st.markdown(
        """
        <div class="action-card">
<div class="action-title"><i class="fa-solid fa-chart-line"></i>Analytics</div>
        <div class="action-desc">View document usage, conversations and system statistics.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Analytics", use_container_width=True, key="analytics"):
        st.switch_page("pages/analytics.py")

# ----------------------------------------------------------------------------
# 4. Recent activity
# ----------------------------------------------------------------------------
st.write("")
st.markdown('<div class="kicker"><span class="dot"></span>Recent Activity</div>', unsafe_allow_html=True)


recent_activity = []

if recent_activity:
    rows_html = ""
    for item in recent_activity:
        rows_html += f"""
        <div class="activity-row">
            <div class="activity-icon">{item['icon']}</div>
            <div class="activity-text">
                <div class="activity-title-row">{item['title']}</div>
                <div class="activity-meta">{item['meta']}</div>
            </div>
            <div class="activity-time">{item['time']}</div>
        </div>
        """
    st.markdown(f'<div class="activity-card">{rows_html}</div>', unsafe_allow_html=True)
else:
    st.markdown(
        '<div class="activity-card"><div class="activity-empty">Upload your first document to begin chatting with AI.</div></div>',
        unsafe_allow_html=True,
    )


db.close()



