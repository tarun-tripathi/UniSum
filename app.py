import streamlit as st
import requests

st.set_page_config(
    page_title="UniSum AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Base */
    .stApp { background-color: #111318; color: #e0e0e0; }

    /* Header */
    .main-header { text-align: center; padding: 2.5rem 0 1.2rem 0; }
    .main-header h1 {
        font-size: 2.6rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .main-header h1 span {
        background: linear-gradient(135deg, #7B6FFF, #38C9C9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .main-header p {
        color: #888;
        font-size: 0.95rem;
        margin-top: 0.5rem;
    }

    /* Feature cards */
    .feature-card {
        background: #1a1d24;
        border: 1px solid #2a2d38;
        border-radius: 10px;
        padding: 1.6rem 1rem;
        text-align: center;
    }
    .feature-card h3 {
        color: #ffffff;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0.4rem 0 0.3rem 0;
    }
    .feature-card p {
        color: #666;
        font-size: 0.82rem;
        margin: 0;
        line-height: 1.5;
    }
    .card-label {
        color: #7B6FFF;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    /* Step label */
    .step-label {
        display: inline-block;
        border: 1px solid #2a2d38;
        border-radius: 4px;
        padding: 0.2rem 0.65rem;
        color: #999;
        font-size: 0.78rem;
        font-weight: 500;
        margin-bottom: 0.7rem;
        letter-spacing: 0.3px;
    }

    /* Answer boxes */
    .answer-box {
        background: #151c1c;
        border: 1px solid #1e3030;
        border-left: 3px solid #38C9C9;
        border-radius: 6px;
        padding: 1.1rem 1.4rem;
        margin-top: 0.8rem;
        color: #d8d8d8;
        font-size: 0.93rem;
        line-height: 1.7;
    }
    .no-answer-box {
        background: #1a1515;
        border: 1px solid #2e1e1e;
        border-left: 3px solid #c0392b;
        border-radius: 6px;
        padding: 1.1rem 1.4rem;
        margin-top: 0.8rem;
        color: #aaa;
        font-size: 0.93rem;
    }

    /* Collection badge */
    .collection-badge {
        background: #13141c;
        border: 1px solid #22253a;
        border-radius: 4px;
        padding: 0.35rem 0.8rem;
        font-family: monospace;
        font-size: 0.72rem;
        color: #5a5a9a;
        word-break: break-all;
        margin: 0.3rem 0 0.8rem 0;
    }

    /* Divider */
    .divider {
        border: none;
        border-top: 1px solid #1e2028;
        margin: 1.2rem 0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0d0f14;
        border-right: 1px solid #1a1d24;
    }
    [data-testid="stSidebar"] * { color: #888 !important; }
    [data-testid="stSidebar"] a { color: #7B6FFF !important; }
    [data-testid="stSidebar"] strong { color: #bbb !important; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #7B6FFF, #38C9C9);
        color: #fff;
        border: none;
        border-radius: 6px;
        padding: 0.45rem 1.2rem;
        font-weight: 600;
        font-size: 0.85rem;
        width: 100%;
        letter-spacing: 0.2px;
        transition: opacity 0.15s;
    }
    .stButton > button:hover { opacity: 0.85; }

    /* Inputs */
    .stTextInput > div > div > input {
        background: #1a1d24;
        border: 1px solid #2a2d38;
        color: #e0e0e0;
        border-radius: 6px;
        font-size: 0.9rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #7B6FFF;
    }
    .stTextInput > div > div > input::placeholder { color: #444; }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #1a1d24;
        border: 1px dashed #2a2d38;
        border-radius: 8px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { border-bottom: 1px solid #1e2028; }
    .stTabs [data-baseweb="tab"] { color: #555; font-size: 0.88rem; padding: 0.5rem 1rem; }
    .stTabs [aria-selected="true"] { color: #e0e0e0 !important; border-bottom: 2px solid #7B6FFF !important; }

    /* Section headings */
    h4 { color: #d0d0d0 !important; font-weight: 600; font-size: 1rem !important; }

    /* Streamlit alerts */
    .stAlert { border-radius: 6px; font-size: 0.88rem; }

    /* Footer */
    .footer {
        text-align: center;
        color: #333;
        font-size: 0.72rem;
        padding: 1.2rem 0 0.5rem 0;
        line-height: 1.8;
    }

    /* Hide streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

API_BASE = "http://localhost:8000"

def check_server():
    try:
        return requests.get(API_BASE, timeout=3).status_code == 200
    except:
        return False

def upload_pdf(file_bytes, filename):
    try:
        r = requests.post(f"{API_BASE}/upload-pdf",
            files={"file": (filename, file_bytes, "application/pdf")}, timeout=60)
        return (r.json().get("message"), None) if r.status_code == 200 else (None, f"Error {r.status_code}")
    except Exception as e:
        return None, str(e)

def query_pdf(col, q):
    try:
        r = requests.post(f"{API_BASE}/pdf-rag",
            json={"collection_name": col, "question": q}, timeout=60)
        return (r.json().get("message"), None) if r.status_code == 200 else (None, f"Error {r.status_code}")
    except Exception as e:
        return None, str(e)

def load_web(url):
    try:
        r = requests.post(f"{API_BASE}/web-rag",
            json={"web_url": url}, timeout=90)
        return (r.json().get("message"), None) if r.status_code == 200 else (None, f"Error {r.status_code}")
    except Exception as e:
        return None, str(e)

def query_web(col, q):
    try:
        r = requests.post(f"{API_BASE}/web-query",
            json={"collection_name": col, "question": q}, timeout=60)
        return (r.json().get("message"), None) if r.status_code == 200 else (None, f"Error {r.status_code}")
    except Exception as e:
        return None, str(e)

# ── Sidebar ──────────────────────────────────────────
with st.sidebar:
    st.markdown("**UniSum AI**")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    server_ok = check_server()
    status_color = "#38C9C9" if server_ok else "#c0392b"
    status_text  = "Online" if server_ok else "Offline"
    st.markdown(f"**Server** &nbsp;<span style='color:{status_color};font-size:0.8rem'>{status_text}</span>",
                unsafe_allow_html=True)
    if server_ok:
        st.markdown("<span style='color:#444;font-size:0.78rem'>localhost:8000</span>",
                    unsafe_allow_html=True)
    else:
        st.markdown("<span style='color:#555;font-size:0.78rem'>Run: python main.py</span>",
                    unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("**How it works**")
    st.markdown("""<div style='color:#555;font-size:0.82rem;line-height:2'>
1. Upload a PDF, URL, or YouTube link<br>
2. Ask any question about the content<br>
3. Get a grounded AI answer
</div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("[API Docs](http://localhost:8000/docs) &nbsp;·&nbsp; [GitHub](https://github.com/tarun-tripathi/UniSum)",
                unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""<div style='color:#2a2a2a;font-size:0.72rem;line-height:1.9'>
Tarun Tripathi<br>Vatsalya Shukla<br>Vishnu Kumar<br>LNCT Bhopal · 2025-26
</div>""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────
st.markdown("""
<div class='main-header'>
    <h1><span>UniSum</span> AI</h1>
    <p>Multi-Source RAG Application &mdash; Ask questions from PDFs, Websites &amp; YouTube</p>
</div>""", unsafe_allow_html=True)

# ── Cards ─────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
for col, label, desc in [
    (c1, "PDF",     "Upload any PDF document and ask questions from its content"),
    (c2, "Web",     "Enter any website URL and query its content instantly"),
    (c3, "YouTube", "Extract transcripts from YouTube and ask questions"),
]:
    with col:
        st.markdown(f"""<div class='feature-card'>
            <div class='card-label'>{label}</div>
            <h3>Q &amp; A</h3>
            <p>{desc}</p>
        </div>""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["PDF Q&A", "Web Q&A", "YouTube Q&A"])

# ── PDF ───────────────────────────────────────────────
with tab1:
    st.markdown("#### Ask questions from a PDF document")
    cl, cr = st.columns(2, gap="large")
    with cl:
        st.markdown("<div class='step-label'>Step 1 — Upload PDF</div>",
                    unsafe_allow_html=True)
        f = st.file_uploader("PDF", type=["pdf"], label_visibility="collapsed")
        if f:
            st.caption(f"{f.name} · {round(f.size/1024,1)} KB")
            if st.button("Process PDF", key="b_pdf"):
                if not server_ok:
                    st.error("Server is offline.")
                else:
                    with st.spinner("Extracting and indexing..."):
                        col_name, err = upload_pdf(f.read(), f.name)
                    if col_name:
                        st.session_state["pdf_col"] = col_name
                        st.success("Indexed successfully.")
                    else:
                        st.error(err)
    with cr:
        st.markdown("<div class='step-label'>Step 2 — Ask a Question</div>",
                    unsafe_allow_html=True)
        if "pdf_col" in st.session_state:
            st.markdown(f"<div class='collection-badge'>{st.session_state['pdf_col']}</div>",
                        unsafe_allow_html=True)
            q = st.text_input("Q", placeholder="e.g. What is the main topic?",
                              key="pdf_q", label_visibility="collapsed")
            if st.button("Get Answer", key="b_pdf_ask"):
                if not q.strip():
                    st.warning("Enter a question.")
                else:
                    with st.spinner("Generating answer..."):
                        ans, err = query_pdf(st.session_state["pdf_col"], q)
                    if ans:
                        if ans.strip().lower() == "no":
                            st.markdown("<div class='no-answer-box'>Answer not found in the document.</div>",
                                        unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='answer-box'><strong>Answer</strong><br><br>{ans}</div>",
                                        unsafe_allow_html=True)
                    else:
                        st.error(err)
        else:
            st.caption("Upload and process a PDF first.")

# ── Web ───────────────────────────────────────────────
with tab2:
    st.markdown("#### Ask questions from any website")
    cl, cr = st.columns(2, gap="large")
    with cl:
        st.markdown("<div class='step-label'>Step 1 — Enter URL</div>",
                    unsafe_allow_html=True)
        url = st.text_input("URL", placeholder="https://example.com",
                            key="web_url", label_visibility="collapsed")
        if st.button("Load Website", key="b_web"):
            if not url.strip():
                st.warning("Enter a URL.")
            elif not server_ok:
                st.error("Server is offline.")
            else:
                with st.spinner("Scraping and indexing..."):
                    col_name, err = load_web(url.strip())
                if col_name:
                    st.session_state["web_col"] = col_name
                    st.session_state["web_url_used"] = url.strip()
                    st.success("Website indexed successfully.")
                else:
                    st.error(err)
    with cr:
        st.markdown("<div class='step-label'>Step 2 — Ask a Question</div>",
                    unsafe_allow_html=True)
        if "web_col" in st.session_state:
            st.caption(st.session_state.get("web_url_used", ""))
            st.markdown(f"<div class='collection-badge'>{st.session_state['web_col']}</div>",
                        unsafe_allow_html=True)
            q = st.text_input("Q", placeholder="e.g. What is this website about?",
                              key="web_q", label_visibility="collapsed")
            if st.button("Get Answer", key="b_web_ask"):
                if not q.strip():
                    st.warning("Enter a question.")
                else:
                    with st.spinner("Generating answer..."):
                        ans, err = query_web(st.session_state["web_col"], q)
                    if ans:
                        if ans.strip().lower() == "no":
                            st.markdown("<div class='no-answer-box'>Answer not found on this page.</div>",
                                        unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='answer-box'><strong>Answer</strong><br><br>{ans}</div>",
                                        unsafe_allow_html=True)
                    else:
                        st.error(err)
        else:
            st.caption("Load a website first.")

# ── YouTube ───────────────────────────────────────────
with tab3:
    st.markdown("#### Ask questions from a YouTube video")
    st.caption("Requires captions to be available on the video.")
    cl, cr = st.columns(2, gap="large")
    with cl:
        st.markdown("<div class='step-label'>Step 1 — Enter YouTube URL</div>",
                    unsafe_allow_html=True)
        yt = st.text_input("YT URL", placeholder="https://youtube.com/watch?v=...",
                           key="yt_url", label_visibility="collapsed")
        if st.button("Load Video", key="b_yt"):
            if not yt.strip():
                st.warning("Enter a YouTube URL.")
            elif not server_ok:
                st.error("Server is offline.")
            else:
                with st.spinner("Extracting transcript..."):
                    try:
                        r = requests.post(f"{API_BASE}/youtube-rag",
                            json={"youtube_url": yt.strip()}, timeout=60)
                        if r.status_code == 200:
                            st.session_state["yt_col"] = r.json().get("message")
                            st.success("Transcript indexed successfully.")
                        else:
                            st.error(f"Error {r.status_code} — Video may not have captions.")
                    except Exception as e:
                        st.error(str(e))
    with cr:
        st.markdown("<div class='step-label'>Step 2 — Ask a Question</div>",
                    unsafe_allow_html=True)
        if "yt_col" in st.session_state:
            st.markdown(f"<div class='collection-badge'>{st.session_state['yt_col']}</div>",
                        unsafe_allow_html=True)
            q = st.text_input("Q", placeholder="e.g. What is explained in this video?",
                              key="yt_q", label_visibility="collapsed")
            if st.button("Get Answer", key="b_yt_ask"):
                if not q.strip():
                    st.warning("Enter a question.")
                else:
                    with st.spinner("Generating answer..."):
                        ans, err = query_web(st.session_state["yt_col"], q)
                    if ans:
                        if ans.strip().lower() == "no":
                            st.markdown("<div class='no-answer-box'>Answer not found in video.</div>",
                                        unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='answer-box'><strong>Answer</strong><br><br>{ans}</div>",
                                        unsafe_allow_html=True)
                    else:
                        st.error(err)
        else:
            st.caption("Load a YouTube video first.")

# ── Footer ────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""<div class='footer'>
UniSum AI &nbsp;|&nbsp; Multi-Source RAG Application &nbsp;|&nbsp;
LNCT Bhopal, Dept. of AI &amp; ML &nbsp;|&nbsp; Session 2025-26<br>
Tarun Tripathi &nbsp;&middot;&nbsp; Vatsalya Shukla &nbsp;&middot;&nbsp; Vishnu Kumar &nbsp;|&nbsp;
Guide: Prof. HARSH NIGAM
</div>""", unsafe_allow_html=True)