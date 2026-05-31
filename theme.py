"""
Lumynary – shared theme injected into every page.
"""

GOOGLE_API_KEY = "AIzaSyAwXsvdxoeaVx8Zqz13TNffF7lsO9xEeQ4"

# ── Google Font import + CSS design system ─────────────────────────────────────
BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & tokens ── */
:root {
    --bg:        #09090f;
    --surface:   #111118;
    --surface2:  #18181f;
    --border:    rgba(255,255,255,0.07);
    --accent:    #7c6aff;
    --accent2:   #ff6ac2;
    --accent3:   #6affda;
    --text:      #e8e8f0;
    --muted:     #6b6b80;
    --radius:    14px;
    --glow:      0 0 40px rgba(124,106,255,0.18);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Typography ── */
h1, h2, h3, .syne { font-family: 'Syne', sans-serif !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.4rem !important;
    transition: transform .15s, box-shadow .15s !important;
    box-shadow: 0 4px 20px rgba(124,106,255,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(124,106,255,0.45) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Inputs ── */
.stTextInput > div > input,
.stTextArea textarea,
.stSelectbox > div,
[data-testid="stFileUploader"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > input:focus,
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(124,106,255,0.2) !important;
}

/* ── DataFrames ── */
[data-testid="stDataFrame"] { border-radius: var(--radius) !important; overflow: hidden; }

/* ── Info / success / warning boxes ── */
.stAlert { border-radius: var(--radius) !important; border: 1px solid var(--border) !important; }

/* ── Tabs ── */
.stTabs [role="tab"] {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    color: var(--muted) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom-color: var(--accent) !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    margin-bottom: .5rem !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    color: var(--text) !important;
    background: var(--surface2) !important;
    border-radius: var(--radius) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ── File uploader drag zone ── */
[data-testid="stFileUploadDropzone"] {
    background: var(--surface2) !important;
    border: 2px dashed var(--accent) !important;
    border-radius: var(--radius) !important;
}

/* ── Slider ── */
[data-testid="stSlider"] .rc-slider-track { background: var(--accent) !important; }
[data-testid="stSlider"] .rc-slider-handle { border-color: var(--accent) !important; }

/* ── Multiselect tags ── */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background: rgba(124,106,255,0.2) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 6px !important;
}

/* ── Number input ── */
.stNumberInput input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}

/* Custom card component */
.lum-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.lum-pill {
    display: inline-block;
    padding: .2rem .75rem;
    border-radius: 999px;
    font-size: .75rem;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
    background: rgba(124,106,255,0.15);
    color: var(--accent);
    border: 1px solid rgba(124,106,255,0.3);
    margin-bottom: .5rem;
}
.lum-hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #fff 30%, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: .5rem;
}
.lum-sub {
    font-family: 'DM Sans', sans-serif;
    color: var(--muted);
    font-size: 1.05rem;
    font-weight: 300;
    margin-bottom: 2rem;
}
.lum-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2rem 0;
}
.lum-stat {
    text-align: center;
    padding: 1.2rem;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
}
.lum-stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.lum-stat-label {
    font-size: .8rem;
    color: var(--muted);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: .08em;
}
.back-btn {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    color: var(--muted) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: .85rem !important;
    font-weight: 600 !important;
    text-decoration: none !important;
    margin-bottom: 1.5rem;
    transition: color .15s;
}
.back-btn:hover { color: var(--text) !important; }

/* Noise overlay for depth */
body::before {
    content: '';
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    z-index: 9999;
    opacity: .4;
}
</style>
"""

PLOTLY_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_family="DM Sans",
    font_color="#e8e8f0",
    colorway=["#7c6aff", "#ff6ac2", "#6affda", "#ffb86c", "#ff5e87", "#50fa7b"],
)

def apply_theme():
    """Call once at the top of every page."""
    import streamlit as st
    st.markdown(BASE_CSS, unsafe_allow_html=True)

def page_header(icon: str, pill: str, title: str, subtitle: str):
    """Render the hero header block used across all sub-pages."""
    import streamlit as st
    st.markdown(f"""
    <div style="padding: 2rem 0 1rem">
        <div class="lum-pill">{icon} &nbsp;{pill}</div>
        <div class="lum-hero-title">{title}</div>
        <p class="lum-sub">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def stat_row(stats: list[tuple]):
    """Render a row of metric cards. stats = [(value, label), ...]"""
    import streamlit as st
    cols = st.columns(len(stats))
    for col, (val, label) in zip(cols, stats):
        col.markdown(f"""
        <div class="lum-stat">
            <div class="lum-stat-val">{val}</div>
            <div class="lum-stat-label">{label}</div>
        </div>""", unsafe_allow_html=True)

def section(title: str):
    import streamlit as st
    st.markdown(f"<hr class='lum-divider'><h3 style='font-family:Syne,sans-serif;font-weight:700;margin-bottom:1rem'>{title}</h3>", unsafe_allow_html=True)
