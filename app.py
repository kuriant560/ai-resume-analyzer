"""
app.py
------
Main entry point for the AI Resume Analyzer.
Run with: streamlit run app.py

This file handles UI only. All logic lives in modules/.
Think of this as the "front door" of the application.
"""

import streamlit as st

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📄 AI Resume Analyzer")
st.markdown(
    "Upload your resume and paste a job description to get an **ATS score**, "
    "skill gap analysis, and personalized improvement suggestions."
)
st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ How to Use")
    st.markdown("""
    1. **Upload** your resume as a PDF
    2. **Paste** the full job description
    3. Click **Analyze Resume**
    4. Review your detailed report
    """)
    st.divider()
    st.info("💡 Tip: Tailor your resume for each job for a higher ATS score.")

# ── Two Column Input Layout ───────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📤 Upload Resume")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Only PDF format supported.",
    )
    if uploaded_file:
        st.success(f"✅ Uploaded: **{uploaded_file.name}**")
        st.caption(f"Size: {uploaded_file.size / 1024:.1f} KB")

with col2:
    st.subheader("📋 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=250,
        placeholder="Copy and paste the full job posting text...",
    )
    word_count = len(job_description.split()) if job_description else 0
    st.caption(f"Word count: {word_count}")

st.divider()

# ── Analyze Button ────────────────────────────────────────────────────────────
analyze_clicked = st.button(
    "🔍 Analyze Resume",
    type="primary",
    use_container_width=True,
    disabled=(uploaded_file is None or len(job_description.strip()) == 0),
)

# ── Analysis Output ───────────────────────────────────────────────────────────
if analyze_clicked:
    with st.spinner("Analyzing your resume... ⏳"):

        from modules.parser import extract_text_from_pdf, get_word_count

        resume_text = extract_text_from_pdf(uploaded_file)

        if not resume_text:
            st.error(
                "❌ Could not extract text from this PDF. "
                "Make sure it is a text-based PDF, not a scanned image."
            )
            st.stop()

        st.success("✅ Resume parsed successfully!")

        with st.expander("📃 View Extracted Resume Text"):
            st.text_area(
                "Raw extracted text:",
                value=resume_text,
                height=300,
                disabled=True,
            )

        st.info(
            f"📊 Resume: **{get_word_count(resume_text)} words**  |  "
            f"Job Description: **{get_word_count(job_description)} words**"
        )

        st.warning(
            "🔧 Full NLP analysis coming in the next step! "
            "Scoring, skill extraction, and dashboard are being built."
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<div style='text-align:center;color:gray;font-size:0.85em;'>"
    "Built with Python · Streamlit · spaCy · scikit-learn"
    "</div>",
    unsafe_allow_html=True,
)