import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from theme import apply_theme, page_header, GOOGLE_API_KEY

import streamlit as st
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

st.set_page_config(
    page_title="CSV Chat · Lumynary",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()

st.markdown("""
<style>
.csv-msg-user {
    background: linear-gradient(135deg, rgba(255,184,108,0.15), rgba(255,106,194,0.08));
    border: 1px solid rgba(255,184,108,0.3);
    border-radius: 16px 16px 4px 16px;
    padding: 1rem 1.2rem;
    margin-left: 3rem;
    font-size: .95rem;
    margin-bottom: .5rem;
}
.csv-msg-ai {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 16px 16px 16px 4px;
    padding: 1rem 1.2rem;
    margin-right: 3rem;
    font-size: .95rem;
    margin-bottom: .5rem;
}
.msg-label-amber { color: #ffcc80; font-family:'Syne',sans-serif; font-size:.7rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase; margin-bottom:.4rem; }
.msg-label-ai    { color: var(--accent); font-family:'Syne',sans-serif; font-size:.7rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase; margin-bottom:.4rem; }

.quick-q {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: .6rem 1rem;
    font-size: .85rem;
    color: var(--muted);
    cursor: pointer;
    transition: all .15s;
    margin-bottom: .4rem;
}
.quick-q:hover { border-color: var(--accent); color: var(--text); }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<a class="back-btn" href="/" style="display:block;margin-bottom:1rem">← Home</a>', unsafe_allow_html=True)
    st.markdown("### 📊 Upload CSV")

    csv_file = st.file_uploader(
        "Upload a CSV file",
        type=["csv"],
        label_visibility="collapsed",
    )

    if csv_file:
        df = pd.read_csv(csv_file)
        st.success(f"✅ {len(df):,} rows · {len(df.columns)} columns")
        st.markdown("**Columns:**")
        for col in df.columns:
            st.markdown(f'<span class="lum-pill" style="margin:.1rem;font-size:.7rem">{col}</span>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.csv_messages = []
        st.rerun()

# ── Main ───────────────────────────────────────────────────────────────────────
page_header(
    icon="💬",
    pill="CSV Chat",
    title="Talk to your CSV",
    subtitle="Ask plain-English questions about your data. Get insights, summaries, and analysis — no SQL needed.",
)

st.markdown('<a class="back-btn" href="/">← Back to Lumynary</a>', unsafe_allow_html=True)

if "csv_messages" not in st.session_state:
    st.session_state.csv_messages = []

# No file state
if not csv_file:
    st.markdown("""
    <div class="lum-card" style="text-align:center;padding:3rem;border-style:dashed">
        <div style="font-size:3rem;margin-bottom:1rem">📊</div>
        <div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;margin-bottom:.5rem">No CSV loaded yet</div>
        <div style="color:var(--muted);font-size:.9rem">Upload a CSV file in the sidebar to start chatting with your data.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Data preview
with st.expander("📋 Data Preview", expanded=False):
    st.dataframe(df, use_container_width=True, height=220)
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", f"{len(df):,}")
    c2.metric("Columns", len(df.columns))
    c3.metric("Missing Values", int(df.isnull().sum().sum()))

st.markdown("<br>", unsafe_allow_html=True)

# Quick question suggestions
if not st.session_state.csv_messages:
    st.markdown("**💡 Try asking:**")
    suggestions = [
        "What is the shape and summary of this dataset?",
        "Which column has the most missing values?",
        "Show me the top 5 rows sorted by the first numeric column.",
        "What are the unique values in each categorical column?",
        "Describe any interesting trends or patterns you see.",
    ]
    for sug in suggestions:
        if st.button(sug, key=sug, use_container_width=True):
            st.session_state.csv_messages.append({"role": "user", "content": sug})
            st.rerun()

# Render history
for msg in st.session_state.csv_messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="csv-msg-user">
            <div class="msg-label-amber">You</div>
            {msg["content"]}
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="msg-label-ai">Lumynary AI</div>', unsafe_allow_html=True)
        st.markdown(msg["content"])
        st.markdown("---")

# Chat input
user_q = st.chat_input("Ask anything about your CSV…")
if user_q:
    st.session_state.csv_messages.append({"role": "user", "content": user_q})
    st.markdown(f"""
    <div class="csv-msg-user">
        <div class="msg-label-amber">You</div>
        {user_q}
    </div>""", unsafe_allow_html=True)

    # Build rich context about the dataframe
    col_types = df.dtypes.to_string()
    sample_rows = df.head(8).to_string()
    desc = df.describe(include="all").to_string()
    missing = df.isnull().sum().to_string()

    system_prompt = f"""You are an expert data analyst assistant. The user has uploaded a CSV dataset.
Here is the dataset context:

SHAPE: {df.shape[0]} rows × {df.shape[1]} columns
COLUMNS & TYPES:
{col_types}

FIRST 8 ROWS:
{sample_rows}

STATISTICAL SUMMARY:
{desc}

MISSING VALUES:
{missing}

Answer the user's question based on this data. Be specific, insightful, and use concrete numbers from the dataset.
Format your answer clearly using markdown. If asked for a chart or visualisation, describe what it would show.
User question: {user_q}"""

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3,
        streaming=True,
    )

    st.markdown('<div class="msg-label-ai">Lumynary AI</div>', unsafe_allow_html=True)
    placeholder = st.empty()
    full_answer = ""

    for chunk in llm.stream(system_prompt):
        if chunk.content:
            full_answer += chunk.content
            placeholder.markdown(full_answer + "▌")

    placeholder.markdown(full_answer)
    st.session_state.csv_messages.append({"role": "assistant", "content": full_answer})

    # Auto-run plotly chart if data warrants it
    numeric_cols = df.select_dtypes("number").columns.tolist()
    if numeric_cols and any(kw in user_q.lower() for kw in ["chart", "plot", "visuali", "graph", "distribution"]):
        import plotly.express as px
        from theme import PLOTLY_THEME
        st.markdown("**📊 Auto-generated visualisation:**")
        col = numeric_cols[0]
        fig = px.histogram(df, x=col, title=f"Distribution of {col}", **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)
