import streamlit as st

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📄 AI Resume Analyzer")
st.markdown(
    "Upload your resume and paste a job description to get an **ATS score**, "
    "skill gap analysis, and personalized improvement suggestions."
)
st.divider()

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

analyze_clicked = st.button(
    "🔍 Analyze Resume",
    type="primary",
    use_container_width=True,
    disabled=(uploaded_file is None or len(job_description.strip()) == 0),
)

if analyze_clicked:
    with st.spinner("Analyzing your resume... ⏳"):

        from modules.parser import extract_text_from_pdf, get_word_count
        from modules.skill_extractor import get_skill_match
        from modules.scorer import calculate_ats_score, generate_suggestions
        from modules.nlp_processor import clean_text
        from modules.visualizer import (
            create_ats_gauge,
            create_score_breakdown_chart,
            create_skill_match_chart,
            create_keyword_bar_chart,
        )

        resume_text = extract_text_from_pdf(uploaded_file)

        if not resume_text:
            st.error(
                "❌ Could not extract text from this PDF. "
                "Make sure it is a text-based PDF, not a scanned image."
            )
            st.stop()

        cleaned_resume = clean_text(resume_text)
        cleaned_jd = clean_text(job_description)
        skill_results = get_skill_match(resume_text, job_description)
        score_results = calculate_ats_score(
            cleaned_resume,
            cleaned_jd,
            skill_results["match_percentage"],
        )
        suggestions = generate_suggestions(
            missing_skills=skill_results["missing_skills"],
            ats_score=score_results["ats_score"],
            text_similarity=score_results["text_similarity"],
            skill_match_percentage=score_results["skill_match_score"],
        )

    st.success("✅ Analysis complete!")
    st.divider()

    # ── Section 1: ATS Score + Gauge ─────────────────────────────────────────
    st.subheader("🎯 ATS Compatibility Score")

    gauge_col, metrics_col = st.columns([1, 1])

    with gauge_col:
        gauge_fig = create_ats_gauge(score_results["ats_score"])
        st.plotly_chart(gauge_fig, use_container_width=True)

    with metrics_col:
        st.markdown("### Score Summary")
        score_col1, score_col2 = st.columns(2)
        with score_col1:
            st.metric("ATS Score", f"{score_results['ats_score']}/100")
            st.metric("Skill Match", f"{score_results['skill_match_score']}%")
        with score_col2:
            st.metric("Text Similarity", f"{score_results['text_similarity']}%")
            st.metric("Keyword Score", f"{score_results['keyword_score']}%")

        ats = score_results["ats_score"]
        if ats >= 80:
            st.success(f"🟢 **{score_results['category']}** — Well optimized!")
        elif ats >= 60:
            st.info(f"🔵 **{score_results['category']}** — Good with room to improve.")
        elif ats >= 40:
            st.warning(f"🟡 **{score_results['category']}** — Needs tailoring.")
        else:
            st.error(f"🔴 **{score_results['category']}** — Significant changes needed.")

    st.divider()

    # ── Section 2: Charts Row ─────────────────────────────────────────────────
    st.subheader("📊 Visual Analysis")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        breakdown_fig = create_score_breakdown_chart(score_results["breakdown"])
        st.plotly_chart(breakdown_fig, use_container_width=True)

    with chart_col2:
        skill_fig = create_skill_match_chart(
            skill_results["matched_skills"],
            skill_results["missing_skills"],
            skill_results["extra_skills"],
        )
        st.plotly_chart(skill_fig, use_container_width=True)

    keyword_fig = create_keyword_bar_chart(cleaned_resume, cleaned_jd)
    st.plotly_chart(keyword_fig, use_container_width=True)

    st.divider()

    # ── Section 3: Skills Analysis ────────────────────────────────────────────
    st.subheader("🛠️ Skills Analysis")

    skills_col1, skills_col2, skills_col3 = st.columns(3)

    with skills_col1:
        st.markdown("### ✅ Matched Skills")
        if skill_results["matched_skills"]:
            for skill in skill_results["matched_skills"]:
                st.success(f"✓ {skill}")
        else:
            st.info("No matching skills found.")

    with skills_col2:
        st.markdown("### ❌ Missing Skills")
        if skill_results["missing_skills"]:
            for skill in skill_results["missing_skills"]:
                st.error(f"✗ {skill}")
        else:
            st.success("No missing skills!")

    with skills_col3:
        st.markdown("### ➕ Extra Skills")
        st.caption("Skills you have beyond what JD requires")
        if skill_results["extra_skills"]:
            for skill in skill_results["extra_skills"]:
                st.info(f"+ {skill}")
        else:
            st.info("No extra skills detected.")

    st.divider()

    # ── Section 4: Suggestions ────────────────────────────────────────────────
    st.subheader("💡 Improvement Suggestions")
    for i, suggestion in enumerate(suggestions, 1):
        st.warning(f"**{i}.** {suggestion}")

    st.divider()

    with st.expander("📃 View Extracted Resume Text"):
        st.text_area(
            "Raw extracted text:",
            value=resume_text,
            height=300,
            disabled=True,
        )

st.divider()
st.markdown(
    "<div style='text-align:center;color:gray;font-size:0.85em;'>"
    "Built with Python · Streamlit · spaCy · scikit-learn · Plotly"
    "</div>",
    unsafe_allow_html=True,
)
