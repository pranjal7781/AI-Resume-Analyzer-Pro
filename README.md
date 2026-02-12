# 🚀 AI Resume Analyzer Pro

AI Resume Analyzer Pro is a web-based application built with Streamlit that analyzes resumes against job descriptions using AI and ATS-style scoring. It provides skill matching, improvement suggestions, resume optimization, and downloadable PDF reports.

---
live here ``https://ai-resume-analyzer-pro.streamlit.app/``
            
## ✨ Features

- 📄 Upload resume in PDF format 
- 📝 Paste job description
- 🤖 AI-based resume analysis
- 📊 ATS-style match score
- ✅ Matched & Missing skills detection
- 📈 Visual skill comparison chart
- ✨ AI-powered resume improvement
- 🗂 Analysis history tracking
- 📑 Export analysis report directly into PDF

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

```
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
```
---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```git clone https://github.com/pranjal7781/AI-Resume-Analyzer.git```
```cd AI-Resume-Analyzer```

### 2️⃣ Create Virtual Environment (Recommended)

```python -m venv venv```

Activate:

For Window:  ```venv\Scripts\activate```

For Linux / Mac: ```source venv/bin/activate```

---

### 3️⃣ Install Dependencies

```pip install -r requirements.txt```

---

###4️⃣ Setup Environment Variables

GROQ_API_KEY=your_api_key_here
```Get API key from: https://console.groq.com``` 

---

▶️ Run the Application

Start the Streamlit app: 

```streamlit run app.py```

Open in browser:
```http://localhost:8501```

---

📖 How to Use

Upload your resume (PDF) 
Paste job description 
Click Analyze
View:
ATS Score
Matched Skills
Missing Skills
Suggestions
Click Improve My Resume for optimized version

Export report using Export to PDF
📑 Output Files

Analysis history stored in:
data/history.csv

PDF reports saved in:
data/
