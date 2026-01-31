from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_resume(resume_text, job_desc):

    prompt = f"""
You are an AI recruiter.

Compare the resume with the job description.

Resume:
{resume_text}

Job Description:
{job_desc}

Give output in this format:

1. Match Percentage
2. Matching Skills
3. Missing Skills
4. Improvement Suggestions
5. ATS Optimization Tips
"""

    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.3,
    max_tokens=800
)


    return response.choices[0].message.content
