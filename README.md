# 🚀 AI Resume Analyzer Pro

AI Resume Analyzer Pro is a web-based application built with Streamlit that analyzes resumes against job descriptions using AI and ATS-style scoring. It provides skill matching, improvement suggestions, resume optimization, and downloadable PDF reports.

---

## ✨ Features

- 📄 Upload resume in PDF format
- 📝 Paste job description
- 🤖 AI-based resume analysis
- 📊 ATS-style match score
- ✅ Matched & Missing skills detection
- 📈 Visual skill comparison chart
- ✨ AI-powered resume improvement
- 🗂 Analysis history tracking
- 📑 Export analysis report as PDF

---

## 🛠 Tech Stack

- Python
- Streamlit
- Pandas
- Matplotlib
- PyPDF2
- ReportLab
- Groq / LLaMA (via API)
- REST API Integration

---

## 📂 Project Structure

AI-Resume-Analyzer/
│
├── app.py
├── requirements.txt
├── matcher.py
├── resume_parser.py
│
├── analyzer/
│ ├── llm.py
│ ├── parser.py
│ ├── scorer.py
│ ├── improver.py
│
├── utils/
│ └── exporter.py
│
└── data/
  └── history.csv


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/pranjal7781/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer

