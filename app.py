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


# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    layout="wide"
)

DATA_DIR = "data"
HISTORY_FILE = f"{DATA_DIR}/history.csv"

os.makedirs(DATA_DIR, exist_ok=True)


# ---------------- SESSION STATE ----------------

if "improved_resume" not in st.session_state:
    st.session_state.improved_resume = ""

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ---------------- UI ----------------

st.title("🚀 AI Resume Analyzer Pro")
st.caption("Analyze your resume against job descriptions using AI")


# ---------------- SIDEBAR ----------------

st.sidebar.header("Upload")

resume_file = st.sidebar.file_uploader(
    "Resume (PDF)",
    type=["pdf"]
)

job_desc = st.sidebar.text_area("Job Description")

analyze_btn = st.sidebar.button("Analyze")


# ---------------- HISTORY ----------------

HISTORY_COLUMNS = ["date", "job_desc", "score", "matched", "missing"]

if os.path.exists(HISTORY_FILE):

    try:
        history_df = pd.read_csv(HISTORY_FILE)

    except:
        history_df = pd.DataFrame(columns=HISTORY_COLUMNS)

else:
    history_df = pd.DataFrame(columns=HISTORY_COLUMNS)


# ---------------- ANALYZE ----------------

if analyze_btn:

    if not resume_file or not job_desc:

        st.warning("Upload resume and enter job description")

    else:

        with st.spinner("Analyzing resume..."):

            # Extract
            resume_text = extract_text(resume_file)

            # AI Analysis
            ai_raw = analyze(resume_text, job_desc)
            result = parse_ai_output(ai_raw)

            score = result.get("score", 0)
            matched = result.get("matched", [])
            missing = result.get("missing", [])
            summary = result.get("summary", "")
            suggestions = result.get("suggestions", [])


            # Save session
            st.session_state.last_result = result


            # Save history
            new_row = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "job_desc": job_desc[:200],
                "score": score,
                "matched": ",".join(matched),
                "missing": ",".join(missing)
            }

            history_df = pd.concat(
                [history_df, pd.DataFrame([new_row])],
                ignore_index=True
            )

            history_df.to_csv(HISTORY_FILE, index=False)

            st.success("Analysis completed!")


# ---------------- SHOW RESULT ----------------

if st.session_state.last_result:

    data = st.session_state.last_result

    score = data["score"]
    matched = data["matched"]
    missing = data["missing"]
    summary = data["summary"]
    suggestions = data["suggestions"]


    st.divider()

    st.subheader("Match Score")
    st.metric("ATS Score", f"{score}%")


    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Matched Skills")
        st.write(matched)

    with col2:
        st.subheader("Missing Skills")
        st.write(missing)


    st.subheader("Summary")
    st.info(summary)


    st.subheader("Suggestions")

    for s in suggestions:
        st.write("•", s)


    # ---------------- IMPROVER ----------------

    st.divider()
    st.subheader("✨ AI Resume Improver")


    if st.button("Improve My Resume"):

        with st.spinner("Improving resume..."):

            improved = improve_resume(
                extract_text(resume_file),
                job_desc
            )

            st.session_state.improved_resume = improved


    if st.session_state.improved_resume:

        st.subheader("📄 Optimized Resume")

        st.text_area(
            "Improved Version",
            st.session_state.improved_resume,
            height=400
        )


    # ---------------- CHART ----------------

    fig, ax = plt.subplots()

    ax.bar(
        ["Matched", "Missing"],
        [len(matched), len(missing)]
    )

    ax.set_title("Skill Comparison")

    st.pyplot(fig)


# ---------------- EXPORT ----------------

if st.session_state.last_result:

    if st.button("📄 Export to PDF"):

        data = st.session_state.last_result

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


# ---------------- HISTORY TABLE ----------------

st.divider()

st.subheader("Previous Analyses")

if not history_df.empty:

    st.dataframe(
        history_df.sort_values("date", ascending=False),
        use_container_width=True
    )

else:
    st.info("No history yet")
