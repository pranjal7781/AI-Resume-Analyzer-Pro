import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from analyzer.parser import extract_text
from analyzer.llm import analyze
from analyzer.scorer import parse_ai_output
from utils.exporter import generate_pdf
from analyzer.improver import improve_resume


# -------------------------------------------------
# Session State (Privacy First)
# -------------------------------------------------

if "resume_text" not in st.session_state:
    st.session_state.resume_text = None

if "job_desc" not in st.session_state:
    st.session_state.job_desc = None

if "improved_resume" not in st.session_state:
    st.session_state.improved_resume = None

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "history" not in st.session_state:
    st.session_state.history = []


# -------------------------------------------------
# App Setup
# -------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    layout="wide"
)

st.title("🚀 AI Resume Analyzer Pro")
st.caption("Analyze your resume against job descriptions using AI")


# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.header("Upload")

resume_file = st.sidebar.file_uploader(
    "Resume (PDF)",
    type=["pdf"]
)

job_desc = st.sidebar.text_area("Job Description")

analyze_btn = st.sidebar.button("Analyze")


# -------------------------------------------------
# Analyze Logic
# -------------------------------------------------

if analyze_btn and resume_file and job_desc:

    with st.spinner("Analyzing resume..."):

        # Extract text
        resume_text = extract_text(resume_file)

        # Save in session
        st.session_state.resume_text = resume_text
        st.session_state.job_desc = job_desc

        # AI Analysis
        ai_raw = analyze(resume_text, job_desc)
        result = parse_ai_output(ai_raw)

        score = result.get("score", 0)
        matched = result.get("matched", [])
        missing = result.get("missing", [])
        summary = result.get("summary", "")
        suggestions = result.get("suggestions", [])

        # Save last result
        st.session_state.last_result = {
            "score": score,
            "matched": matched,
            "missing": missing,
            "summary": summary,
            "suggestions": suggestions
        }

        # Save private session history
        new_row = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "job_desc": job_desc[:200],
            "score": score,
            "matched": ", ".join(matched),
            "missing": ", ".join(missing)
        }

        st.session_state.history.append(new_row)

        st.success("Analysis completed!")


# -------------------------------------------------
# Display Result
# -------------------------------------------------

if st.session_state.last_result:

    data = st.session_state.last_result

    score = data["score"]
    matched = data["matched"]
    missing = data["missing"]
    summary = data["summary"]
    suggestions = data["suggestions"]

    st.subheader("📊 Match Score")
    st.metric("ATS Score", f"{score}%")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matched Skills")
        st.write(matched)

    with col2:
        st.subheader("❌ Missing Skills")
        st.write(missing)

    st.subheader("📝 Summary")
    st.info(summary)

    st.subheader("💡 Suggestions")

    for s in suggestions:
        st.write("•", s)


    # -------------------------------
    # Resume Improver
    # -------------------------------

    st.divider()
    st.subheader("✨ AI Resume Improver")

    if st.button("Improve My Resume"):

        if st.session_state.resume_text and st.session_state.job_desc:

            with st.spinner("Improving resume..."):

                improved = improve_resume(
                    st.session_state.resume_text,
                    st.session_state.job_desc
                )

                st.session_state.improved_resume = improved

        else:
            st.warning("Please analyze resume first.")


    if st.session_state.improved_resume:

        st.subheader("📄 Optimized Resume")

        st.text_area(
            "Improved Version",
            st.session_state.improved_resume,
            height=400
        )


    # -------------------------------
    # Chart
    # -------------------------------

    fig, ax = plt.subplots()

    ax.bar(
        ["Matched", "Missing"],
        [len(matched), len(missing)]
    )

    ax.set_title("Skill Comparison")

    st.pyplot(fig)


# -------------------------------------------------
# Export PDF
# -------------------------------------------------

st.divider()

if st.button("📄 Export to PDF"):

    data = st.session_state.last_result

    if not data:
        st.warning("Please analyze resume first.")

    else:

        path = generate_pdf(
            data["score"],
            data["matched"],
            data["missing"],
            data["summary"],
            data["suggestions"]
        )

        with open(path, "rb") as f:

            st.download_button(
                "⬇ Download Report",
                f,
                file_name="resume_report.pdf",
                mime="application/pdf"
            )


# -------------------------------------------------
# Private History (Session Only)
# -------------------------------------------------

st.divider()
st.subheader("📜 Previous Analyses (This Session Only)")

if st.session_state.history:

    df = pd.DataFrame(st.session_state.history)

    st.dataframe(
        df.sort_values("date", ascending=False),
        use_container_width=True
    )

else:
    st.info("No analyses in this session.")
