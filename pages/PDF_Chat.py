import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from theme import apply_theme, page_header, GOOGLE_API_KEY

import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import google.generativeai as genai

# ── Config ─────────────────────────────────────────────────────────────────────
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(
    page_title="PDF Chat · Lumynary",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()

# Extra PDF-page styles
st.markdown("""
<style>
/* Sidebar upload zone */
.upload-header {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: .75rem;
    color: var(--text);
}
/* Chat container */
.chat-wrap {
    display: flex;
    flex-direction: column;
    gap: .75rem;
    padding-bottom: 1rem;
}
.msg-user {
    background: linear-gradient(135deg, rgba(124,106,255,0.18), rgba(255,106,194,0.10));
    border: 1px solid rgba(124,106,255,0.3);
    border-radius: 16px 16px 4px 16px;
    padding: 1rem 1.2rem;
    margin-left: 4rem;
    font-size: .95rem;
}
.msg-ai {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 16px 16px 16px 4px;
    padding: 1rem 1.2rem;
    margin-right: 4rem;
    font-size: .95rem;
}
.msg-label {
    font-family: 'Syne', sans-serif;
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
    margin-bottom: .4rem;
    color: var(--muted);
}
.msg-user .msg-label { color: #a89fff; text-align: right; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
def get_pdf_text(pdfs):
    text = ""
    for pdf in pdfs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    return text

def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return splitter.split_text(text)

def build_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )
    vs = FAISS.from_texts(chunks, embedding=embeddings)
    vs.save_local("faiss_index")
    return vs

def get_chain():
    template = """
You are a precise document assistant. Answer the question thoroughly using ONLY the provided context.
If the answer is not in the context, say "This information isn't in the uploaded documents."
Be clear, structured, and helpful.

Context:
{context}

Question:
{question}

Answer:"""
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2,
        streaming=True,
    )
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    return load_qa_chain(llm=llm, chain_type="stuff", prompt=prompt)

def answer_question_streaming(question, placeholder):
    """Query FAISS + stream the answer token-by-token."""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )
    try:
        vs = FAISS.load_local(
            "faiss_index", embeddings, allow_dangerous_deserialization=True
        )
    except Exception:
        placeholder.error("⚠️ Please process your PDFs first using the sidebar.")
        return None

    docs = vs.similarity_search(question, k=5)

    # Build context manually so we can stream
    context = "\n\n".join(d.page_content for d in docs)
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2,
        streaming=True,
    )
    system = f"""You are a precise document assistant. Answer the question thoroughly using ONLY the provided context.
If the answer is not in the context, say "This information isn't in the uploaded documents."

Context:
{context}"""

    full = ""
    for chunk in llm.stream(f"{system}\n\nQuestion: {question}\n\nAnswer:"):
        full += chunk.content
        placeholder.markdown(full + "▌")
    placeholder.markdown(full)
    return full

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<a class="back-btn" href="/" style="display:block;margin-bottom:1rem">← Home</a>', unsafe_allow_html=True)
    st.markdown('<p class="upload-header">📄 Upload PDFs</p>', unsafe_allow_html=True)

    pdf_docs = st.file_uploader(
        "Add one or more PDF files",
        accept_multiple_files=True,
        type=["pdf"],
        label_visibility="collapsed",
    )

    if pdf_docs:
        st.success(f"{len(pdf_docs)} file(s) ready")

    if st.button("⚡ Process & Index", type="primary", use_container_width=True, disabled=not pdf_docs):
        with st.spinner("Extracting & indexing…"):
            raw = get_pdf_text(pdf_docs)
            if not raw.strip():
                st.error("No readable text found. Try a different PDF.")
            else:
                chunks = get_text_chunks(raw)
                build_vector_store(chunks)
                st.session_state["indexed"] = True
                st.success(f"✅ Indexed {len(chunks)} chunks")

    st.markdown("---")
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Status badge
    if st.session_state.get("indexed"):
        st.markdown('<div class="lum-pill">✓ Index ready</div>', unsafe_allow_html=True)
    else:
        st.caption("Upload & process PDFs to start chatting.")

# ── Main ───────────────────────────────────────────────────────────────────────
page_header(
    icon="📄",
    pill="PDF Chat",
    title="Chat with your PDFs",
    subtitle="Ask anything about your uploaded documents. Answers are grounded in the actual content.",
)

# Init chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-user">
            <div class="msg-label">You</div>
            {msg["content"]}
        </div>""", unsafe_allow_html=True)
    else:
        with st.container():
            st.markdown('<div class="msg-label" style="color:var(--accent);font-family:Syne,sans-serif;font-size:.7rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.3rem">Lumynary AI</div>', unsafe_allow_html=True)
            st.markdown(msg["content"])
            st.markdown("---")

# Empty state
if not st.session_state.messages:
    st.markdown("""
    <div class="lum-card" style="text-align:center;padding:3rem">
        <div style="font-size:3rem;margin-bottom:1rem">💬</div>
        <div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;margin-bottom:.5rem">Ready to chat</div>
        <div style="color:var(--muted);font-size:.9rem">Upload &amp; process PDFs in the sidebar, then ask a question below.</div>
    </div>
    """, unsafe_allow_html=True)

# Chat input
prompt = st.chat_input("Ask a question about your PDFs…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"""
    <div class="msg-user">
        <div class="msg-label">You</div>
        {prompt}
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="msg-label" style="color:var(--accent);font-family:Syne,sans-serif;font-size:.7rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.3rem;margin-top:.5rem">Lumynary AI</div>', unsafe_allow_html=True)
    placeholder = st.empty()

    answer = answer_question_streaming(prompt, placeholder)
    if answer:
        st.session_state.messages.append({"role": "assistant", "content": answer})
