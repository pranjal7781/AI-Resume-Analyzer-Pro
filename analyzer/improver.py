from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def improve_resume(resume_text, job_desc):

    prompt = f"""
You are a professional resume writer and ATS expert.

Improve the following resume to better match the job description.

Rules:
- Rewrite weak bullet points
- Add measurable impact where possible
- Optimize for ATS keywords
- Keep it truthful
- Do NOT invent experience

Return improved resume text only.

Resume:
{resume_text}

Job Description:
{job_desc}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=900
    )

    return response.choices[0].message.content.strip()
