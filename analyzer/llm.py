import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze(resume_text, jd_text):

    prompt = f"""
Compare this resume and job description.

Return STRICT JSON:

{{
 "score": number (0-100),
 "matched": [skills],
 "missing": [skills],
 "summary": "text",
 "suggestions": ["text"]
}}

Resume:
{resume_text}

Job:
{jd_text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=800
    )

    return response.choices[0].message.content
