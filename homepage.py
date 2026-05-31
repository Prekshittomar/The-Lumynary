import streamlit as st
from theme import apply_theme, BASE_CSS

st.set_page_config(
    page_title="Lumynary – AI Suite",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_theme()

# ── Extra homepage-specific CSS ────────────────────────────────────────────────
st.markdown("""
<style>
.nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: .75rem 0 2.5rem;
}
.nav-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7c6aff, #ff6ac2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -.02em;
}
.nav-tag {
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .1em;
    color: var(--muted);
    text-transform: uppercase;
    border: 1px solid var(--border);
    padding: .25rem .7rem;
    border-radius: 999px;
}
/* Hero */
.hero-wrap {
    text-align: center;
    padding: 3.5rem 0 2rem;
    max-width: 780px;
    margin: 0 auto;
}
.hero-badge {
    display: inline-block;
    background: rgba(124,106,255,0.12);
    border: 1px solid rgba(124,106,255,0.35);
    color: #a89fff;
    font-family: 'Syne', sans-serif;
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    padding: .35rem 1rem;
    border-radius: 999px;
    margin-bottom: 1.5rem;
}
.hero-h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 4.8rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -.03em;
    margin-bottom: 1.1rem;
}
.hero-h1 span.grad {
    background: linear-gradient(135deg, #7c6aff 0%, #ff6ac2 50%, #6affda 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-desc {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.15rem;
    font-weight: 300;
    color: #7a7a90;
    line-height: 1.7;
    max-width: 560px;
    margin: 0 auto 2.5rem;
}

/* Tool cards */
.tool-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; }
.tool-card {
    position: relative;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 2rem 2rem 1.6rem;
    cursor: pointer;
    transition: transform .2s, border-color .2s, box-shadow .2s;
    overflow: hidden;
}
.tool-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 18px;
    opacity: 0;
    transition: opacity .2s;
}
.tool-card.c1::before { background: radial-gradient(circle at top left, rgba(124,106,255,0.12), transparent 60%); }
.tool-card.c2::before { background: radial-gradient(circle at top left, rgba(255,106,194,0.12), transparent 60%); }
.tool-card.c3::before { background: radial-gradient(circle at top left, rgba(106,255,218,0.12), transparent 60%); }
.tool-card.c4::before { background: radial-gradient(circle at top left, rgba(255,184,108,0.12), transparent 60%); }
.tool-card:hover { transform: translateY(-4px); border-color: rgba(255,255,255,0.14); box-shadow: 0 20px 60px rgba(0,0,0,0.4); }
.tool-card:hover::before { opacity: 1; }

.tool-icon {
    font-size: 2.2rem;
    margin-bottom: 1rem;
    display: block;
    filter: drop-shadow(0 0 12px currentColor);
}
.tool-name {
    font-family: 'Syne', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: .4rem;
}
.tool-desc {
    font-size: .88rem;
    color: var(--muted);
    line-height: 1.6;
    margin-bottom: 1.4rem;
}
.tool-tag-row { display: flex; gap: .4rem; flex-wrap: wrap; }
.tool-tag {
    font-size: .7rem;
    font-weight: 600;
    letter-spacing: .06em;
    text-transform: uppercase;
    padding: .2rem .6rem;
    border-radius: 999px;
    border: 1px solid;
}
.tag-violet { color: #a89fff; border-color: rgba(124,106,255,0.4); background: rgba(124,106,255,0.08); }
.tag-pink   { color: #ff9ed6; border-color: rgba(255,106,194,0.4); background: rgba(255,106,194,0.08); }
.tag-teal   { color: #6affda; border-color: rgba(106,255,218,0.4); background: rgba(106,255,218,0.08); }
.tag-amber  { color: #ffcc80; border-color: rgba(255,184,108,0.4); background: rgba(255,184,108,0.08); }

/* Glow blobs */
.blob {
    position: fixed;
    border-radius: 50%;
    filter: blur(120px);
    pointer-events: none;
    z-index: 0;
    opacity: .35;
}
.blob1 { width: 600px; height: 600px; background: #7c6aff; top: -200px; left: -200px; }
.blob2 { width: 500px; height: 500px; background: #ff6ac2; bottom: -150px; right: -150px; }
.blob3 { width: 300px; height: 300px; background: #6affda; top: 50%; left: 50%; transform: translate(-50%,-50%); }

/* Footer */
.footer {
    text-align: center;
    padding: 3rem 0 1rem;
    color: var(--muted);
    font-size: .8rem;
}
.footer span { color: var(--accent); }
</style>

<!-- Ambient blobs -->
<div class="blob blob1"></div>
<div class="blob blob2"></div>
<div class="blob blob3"></div>
""", unsafe_allow_html=True)

# ── Nav ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
    <div class="nav-logo">✦ Lumynary</div>
    <div class="nav-tag">AI Productivity Suite</div>
</div>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">✦ &nbsp; Powered by Gemini &nbsp; ✦</div>
    <div class="hero-h1">
        Your intelligence,<br><span class="grad">amplified.</span>
    </div>
    <p class="hero-desc">
        Four AI-powered tools. One seamless workspace. Analyze data, chat with documents,
        generate recipes, and query CSV files — all in one place.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Tool Cards ─────────────────────────────────────────────────────────────────
TOOLS = [
    {
        "key": "data",
        "cls": "c1",
        "icon": "📊",
        "name": "Smart Data Analysis",
        "desc": "Upload any CSV or Excel file and instantly explore statistics, visualize distributions, and run group-by aggregations with beautiful interactive charts.",
        "tags": [("tag-violet", "CSV / Excel"), ("tag-violet", "Plotly Charts"), ("tag-violet", "Statistics")],
        "page": "pages/Data_Analysis.py",
    },
    {
        "key": "pdf",
        "cls": "c2",
        "icon": "📄",
        "name": "Chat with PDF",
        "desc": "Upload one or multiple PDFs and have a natural conversation with your documents. Powered by vector search and Gemini for pinpoint accurate answers.",
        "tags": [("tag-pink", "RAG"), ("tag-pink", "Multi-PDF"), ("tag-pink", "Gemini")],
        "page": "pages/PDF_Chat.py",
    },
    {
        "key": "recipe",
        "cls": "c3",
        "icon": "🍽️",
        "name": "Food Recipe Generator",
        "desc": "Snap a photo of any food or ingredient and let Gemini Vision craft a detailed recipe with ingredients, steps, and cooking tips — streamed in real time.",
        "tags": [("tag-teal", "Vision AI"), ("tag-teal", "Streaming"), ("tag-teal", "Gemini")],
        "page": "pages/Recipe_Generator.py",
    },
    {
        "key": "csv",
        "cls": "c4",
        "icon": "💬",
        "name": "Chat with CSV",
        "desc": "Ask plain-English questions about your CSV data. The AI understands your columns, runs analysis, and returns charts or summaries — no SQL needed.",
        "tags": [("tag-amber", "PandasAI"), ("tag-amber", "NL Queries"), ("tag-amber", "Auto Charts")],
        "page": "pages/CSV_Chat.py",
    },
]

col1, col2 = st.columns(2, gap="medium")
cols = [col1, col2, col1, col2]

for tool, col in zip(TOOLS, cols):
    with col:
        tag_html = "".join(
            f'<span class="tool-tag {tc}">{tl}</span>' for tc, tl in tool["tags"]
        )
        st.markdown(f"""
        <div class="tool-card {tool['cls']}">
            <span class="tool-icon">{tool['icon']}</span>
            <div class="tool-name">{tool['name']}</div>
            <p class="tool-desc">{tool['desc']}</p>
            <div class="tool-tag-row">{tag_html}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Open {tool['name']} →", key=tool["key"], use_container_width=True):
            st.switch_page(tool["page"])

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built with <span>♥</span> using Streamlit &amp; Gemini &nbsp;·&nbsp; Lumynary AI Suite
</div>
""", unsafe_allow_html=True)
