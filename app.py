"""
app.py
------
Main entry point for the AI Resume Analyzer.
Run with: streamlit run app.py
"""

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

    st.subheader("🎯 ATS Compatibility Score")
    score_col1, score_col2, score_col3, score_col4 = st.columns(4)

    with score_col1:
        st.metric(label="ATS Score", value=f"{score_results['ats_score']}/100")
    with score_col2:
        st.metric(label="Skill Match", value=f"{score_results['skill_match_score']}%")
    with score_col3:
        st.metric(label="Text Similarity", value=f"{score_results['text_similarity']}%")
    with score_col4:
        st.metric(label="Keyword Score", value=f"{score_results['keyword_score']}%")

    ats = score_results["ats_score"]
    if ats >= 80:
        st.success(f"🟢 **{score_results['category']}** — Your resume is well optimized!")
    elif ats >= 60:
        st.info(f"🔵 **{score_results['category']}** — Good match with room for improvement.")
    elif ats >= 40:
        st.warning(f"🟡 **{score_results['category']}** — Moderate match. Consider tailoring.")
    else:
        st.error(f"🔴 **{score_results['category']}** — Low match. Significant changes needed.")

    st.progress(int(ats))
    st.divider()

    st.subheader("📊 Score Breakdown")
    b = score_results["breakdown"]
    breakdown_col1, breakdown_col2, breakdown_col3 = st.columns(3)

    with breakdown_col1:
        st.metric("Skill Contribution (50%)", f"{b['skill_match_contribution']}")
    with breakdown_col2:
        st.metric("Similarity Contribution (40%)", f"{b['similarity_contribution']}")
    with breakdown_col3:
        st.metric("Keyword Contribution (10%)", f"{b['keyword_contribution']}")

    st.divider()

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
    "Built with Python · Streamlit · spaCy · scikit-learn"
    "</div>",
    unsafe_allow_html=True,
)
