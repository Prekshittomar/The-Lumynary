import os, sys, io, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from theme import apply_theme, page_header, GOOGLE_API_KEY

import streamlit as st
import PIL.Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

st.set_page_config(
    page_title="Recipe Generator · Lumynary",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_theme()

st.markdown("""
<style>
.recipe-output {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 2rem;
    margin-top: 1.5rem;
    line-height: 1.8;
}
.recipe-output h1, .recipe-output h2, .recipe-output h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    margin-top: 1.5rem !important;
}
.recipe-output h2 {
    background: linear-gradient(135deg, #7c6aff, #ff6ac2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.img-frame {
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid var(--border);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.style-chip {
    display: inline-block;
    padding: .35rem .9rem;
    border-radius: 999px;
    font-size: .82rem;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
    border: 1px solid var(--border);
    color: var(--muted);
    cursor: pointer;
    transition: all .15s;
    margin: .2rem;
}
.style-chip:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: rgba(124,106,255,0.08);
}
.cuisine-grid {
    display: flex;
    flex-wrap: wrap;
    gap: .4rem;
    margin: .5rem 0 1rem;
}
</style>
""", unsafe_allow_html=True)

page_header(
    icon="🍽️",
    pill="Recipe Generator",
    title="Food to Recipe, Instantly",
    subtitle="Upload a photo of any dish or ingredient — Gemini Vision will craft a detailed recipe streamed in real time.",
)

st.markdown('<a class="back-btn" href="/">← Back to Lumynary</a>', unsafe_allow_html=True)

# ── Layout ─────────────────────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("### 📸 Upload Food Image")
    uploaded = st.file_uploader(
        "Photo of your food or ingredients",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
    )

    if uploaded:
        img = PIL.Image.open(uploaded)
        st.markdown('<div class="img-frame">', unsafe_allow_html=True)
        st.image(img, use_column_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("### ⚙️ Customise Your Recipe")

    # Cuisine quick-picks
    st.markdown("**Cuisine style** *(click to fill prompt)*")
    cuisines = ["🇮🇹 Italian", "🇯🇵 Japanese", "🇲🇽 Mexican", "🇮🇳 Indian",
                "🇫🇷 French", "🇹🇭 Thai", "🇲🇦 Mediterranean", "🇺🇸 American"]
    cuisine_html = "".join(f'<span class="style-chip">{c}</span>' for c in cuisines)
    st.markdown(f'<div class="cuisine-grid">{cuisine_html}</div>', unsafe_allow_html=True)

    prompt = st.text_area(
        "Describe what you want",
        value="Identify the dish or ingredients in this image and provide a complete recipe with:\n- Dish name & brief description\n- Full ingredient list with measurements\n- Step-by-step cooking instructions\n- Cooking time, serving size & difficulty level\n- Pro tips & possible variations",
        height=180,
        help="Customise the prompt to get the recipe format you want.",
    )

    c1, c2 = st.columns(2)
    with c1:
        servings = st.selectbox("Servings", [1, 2, 4, 6, 8, 10, 12], index=2)
    with c2:
        difficulty = st.selectbox("Difficulty", ["Any", "Easy", "Medium", "Advanced"])

    extra = ""
    if servings:
        extra += f" Scale the recipe for {servings} servings."
    if difficulty != "Any":
        extra += f" Keep it {difficulty.lower()} difficulty."

    generate = st.button(
        "✨ Generate Recipe",
        type="primary",
        use_container_width=True,
        disabled=uploaded is None,
    )

# ── Generation ─────────────────────────────────────────────────────────────────
if generate and uploaded:
    img = PIL.Image.open(uploaded).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    b64 = base64.b64encode(buf.getvalue()).decode()
    image_data_url = f"data:image/jpeg;base64,{b64}"

    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.7,
        streaming=True,
    )

    message = HumanMessage(content=[
        {"type": "text",      "text": prompt + extra},
        {"type": "image_url", "image_url": image_data_url},
    ])

    st.markdown('<hr class="lum-divider">', unsafe_allow_html=True)
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.3rem;font-weight:700;margin-bottom:1rem">🧑‍🍳 Your Recipe</div>', unsafe_allow_html=True)

    output_area = st.empty()
    full_text = ""

    with st.spinner("Gemini Vision is analysing your image…"):
        for chunk in model.stream([message]):
            if chunk.content:
                full_text += chunk.content
                output_area.markdown(
                    f'<div class="recipe-output">{full_text}▌</div>',
                    unsafe_allow_html=True,
                )

    # Final render without cursor
    output_area.markdown(
        f'<div class="recipe-output">{full_text}</div>',
        unsafe_allow_html=True,
    )

    # Download button
    st.download_button(
        "⬇️ Download Recipe (Markdown)",
        data=full_text,
        file_name="lumynary_recipe.md",
        mime="text/markdown",
    )

elif not uploaded:
    st.markdown("""
    <div class="lum-card" style="text-align:center;padding:3rem;border-style:dashed">
        <div style="font-size:3rem;margin-bottom:1rem">📷</div>
        <div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;margin-bottom:.5rem">Upload a food image to begin</div>
        <div style="color:var(--muted);font-size:.9rem">JPG, JPEG, PNG or WEBP formats supported</div>
    </div>
    """, unsafe_allow_html=True)
