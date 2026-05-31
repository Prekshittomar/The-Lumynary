import pandas as pd
import streamlit as st
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from theme import apply_theme, PLOTLY_THEME, page_header, stat_row, section

st.set_page_config(
    page_title="Data Analysis · Lumynary",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_theme()

page_header(
    icon="📊",
    pill="Data Analysis",
    title="Smart Data Explorer",
    subtitle="Upload any CSV or Excel file and instantly surface insights, statistics, and beautiful visualisations.",
)

# ── Back link ──────────────────────────────────────────────────────────────────
st.markdown('<a class="back-btn" href="/">← Back to Lumynary</a>', unsafe_allow_html=True)

# ── File Upload ────────────────────────────────────────────────────────────────
file = st.file_uploader(
    "Drop your CSV or Excel file here",
    type=["csv", "xlsx"],
    help="Supported formats: .csv, .xlsx",
)

if file is None:
    st.markdown("""
    <div class="lum-card" style="text-align:center;padding:3rem;border-style:dashed">
        <div style="font-size:3rem;margin-bottom:1rem">📂</div>
        <div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;margin-bottom:.5rem">No file uploaded yet</div>
        <div style="color:var(--muted);font-size:.9rem">Drag & drop a CSV or Excel file above to get started</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Load Data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(f):
    return pd.read_csv(f) if f.name.endswith("csv") else pd.read_excel(f)

data = load_data(file)

# ── Quick Stats ────────────────────────────────────────────────────────────────
n_missing  = int(data.isnull().sum().sum())
n_numeric  = int(data.select_dtypes("number").shape[1])
dupe_rows  = int(data.duplicated().sum())

stat_row([
    (f"{data.shape[0]:,}", "Rows"),
    (f"{data.shape[1]}", "Columns"),
    (f"{n_numeric}", "Numeric cols"),
    (f"{n_missing:,}", "Missing values"),
    (f"{dupe_rows:,}", "Duplicate rows"),
])

st.markdown("<br>", unsafe_allow_html=True)
st.dataframe(data, use_container_width=True, height=280)
st.success(f"✅ **{file.name}** loaded successfully", icon=None)

# ── Basic Analysis Tabs ────────────────────────────────────────────────────────
section("Dataset Overview")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Statistics", "🔼 Top / Bottom Rows", "🗂 Data Types", "🏷 Columns", "🕳 Missing Values",
])

with tab1:
    st.dataframe(data.describe().T.style.background_gradient(cmap="Purples"), use_container_width=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Top Rows**")
        n = st.slider("Rows", 1, min(data.shape[0], 100), 5, key="top")
        st.dataframe(data.head(n), use_container_width=True)
    with c2:
        st.markdown("**Bottom Rows**")
        n2 = st.slider("Rows", 1, min(data.shape[0], 100), 5, key="bot")
        st.dataframe(data.tail(n2), use_container_width=True)

with tab3:
    dtype_df = data.dtypes.reset_index()
    dtype_df.columns = ["Column", "Data Type"]
    dtype_df["Data Type"] = dtype_df["Data Type"].astype(str)
    st.dataframe(dtype_df, use_container_width=True)

with tab4:
    cols_list = list(data.columns)
    html_cols = "".join(
        f'<span class="lum-pill" style="margin:.2rem">{c}</span>' for c in cols_list
    )
    st.markdown(f'<div style="line-height:2.5">{html_cols}</div>', unsafe_allow_html=True)

with tab5:
    missing = data.isnull().sum().reset_index()
    missing.columns = ["Column", "Missing Count"]
    missing["Missing %"] = (missing["Missing Count"] / len(data) * 100).round(2)
    missing = missing[missing["Missing Count"] > 0]
    if missing.empty:
        st.success("🎉 No missing values — your dataset is clean!")
    else:
        st.dataframe(missing, use_container_width=True)
        fig = px.bar(
            missing, x="Column", y="Missing %",
            title="Missing Value Distribution",
            **PLOTLY_THEME,
        )
        st.plotly_chart(fig, use_container_width=True)

# ── Value Counts ───────────────────────────────────────────────────────────────
section("Column Value Counts")
with st.expander("Explore value distribution for a column", expanded=False):
    c1, c2 = st.columns([3, 1])
    with c1:
        column = st.selectbox("Column", options=list(data.columns), key="vc_col")
    with c2:
        topn = st.number_input("Top N", min_value=1, value=10, step=1)

    if st.button("Analyse Column", type="primary"):
        result = data[column].value_counts().reset_index().head(int(topn))
        result.columns = [column, "count"]
        st.dataframe(result, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            fig = px.bar(result, x=column, y="count", text="count",
                         title="Bar Chart", **PLOTLY_THEME)
            fig.update_traces(marker_color="#7c6aff", textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.pie(result, names=column, values="count",
                         title="Pie Chart", **PLOTLY_THEME)
            st.plotly_chart(fig, use_container_width=True)
        with c3:
            fig = px.line(result, x=column, y="count", markers=True,
                          title="Line Chart", **PLOTLY_THEME)
            fig.update_traces(line_color="#ff6ac2", marker_color="#ff6ac2")
            st.plotly_chart(fig, use_container_width=True)

# ── Group By ───────────────────────────────────────────────────────────────────
section("Group-By Analysis")
st.markdown('<p class="lum-sub" style="margin-top:-.5rem">Aggregate your data by one or more columns and visualise the result.</p>', unsafe_allow_html=True)

with st.expander("Configure Group-By", expanded=False):
    c1, c2, c3 = st.columns(3)
    with c1:
        groupby_cols = st.multiselect("Group by columns", options=list(data.columns))
    with c2:
        agg_col = st.selectbox("Column to aggregate", options=list(data.columns), key="agg_col")
    with c3:
        operation = st.selectbox(
            "Aggregation function",
            options=["sum", "mean", "median", "max", "min", "count", "std"],
        )

    if not groupby_cols:
        st.info("Select at least one column to group by.")
        st.stop()

    result = (
        data.groupby(groupby_cols)
        .agg(value=(agg_col, operation))
        .reset_index()
        .rename(columns={"value": f"{operation}_{agg_col}"})
    )
    agg_label = f"{operation}_{agg_col}"

    st.dataframe(result, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    chart_type = st.selectbox(
        "Visualisation type",
        options=["bar", "line", "scatter", "pie", "sunburst"],
        key="chart_type",
    )

    if chart_type in ("bar", "line", "scatter"):
        c1, c2, c3 = st.columns(3)
        with c1: x_axis = st.selectbox("X axis", options=list(result.columns), key="xax")
        with c2: y_axis = st.selectbox("Y axis", options=list(result.columns), key="yax")
        with c3: color  = st.selectbox("Color by", options=[None] + list(result.columns), key="col")

    if chart_type == "bar":
        facet = st.selectbox("Facet column (optional)", options=[None] + list(result.columns))
        fig = px.bar(result, x=x_axis, y=y_axis, color=color,
                     facet_col=facet, barmode="group", title="Bar Chart", **PLOTLY_THEME)
    elif chart_type == "line":
        fig = px.line(result, x=x_axis, y=y_axis, color=color,
                      markers=True, title="Line Chart", **PLOTLY_THEME)
    elif chart_type == "scatter":
        size_col = st.selectbox("Bubble size (numeric)", options=[None] + list(result.columns))
        if size_col and not pd.api.types.is_numeric_dtype(result[size_col]):
            st.warning("Size column must be numeric.")
            size_col = None
        fig = px.scatter(result, x=x_axis, y=y_axis, color=color,
                         size=size_col, title="Scatter Plot", **PLOTLY_THEME)
    elif chart_type == "pie":
        c1, c2 = st.columns(2)
        with c1: vals  = st.selectbox("Values", options=list(result.columns), key="pv")
        with c2: names = st.selectbox("Labels", options=list(result.columns), key="pn")
        fig = px.pie(result, values=vals, names=names, title="Pie Chart", **PLOTLY_THEME)
    elif chart_type == "sunburst":
        path = st.multiselect("Hierarchy path", options=list(result.columns))
        if not path:
            st.info("Select at least one path column.")
            st.stop()
        fig = px.sunburst(result, path=path, values=agg_label,
                          title="Sunburst Chart", **PLOTLY_THEME)

    st.plotly_chart(fig, use_container_width=True)
