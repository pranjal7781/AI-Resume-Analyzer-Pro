import json
import re


def parse_ai_output(text):

    try:
        match = re.search(r"\{.*\}", text, re.S)

        if not match:
            raise ValueError("No JSON found")

        data = json.loads(match.group())

    except Exception:

        # Fallback
        data = {
            "score": 0,
            "matched": [],
            "missing": [],
            "summary": "AI parsing failed",
            "suggestions": []
        }

    # Normalize keys
    return {
        "score": int(data.get("score", 0)),
        "matched": data.get("matched", []),
        "missing": data.get("missing", []),
        "summary": data.get("summary", ""),
        "suggestions": data.get("suggestions", [])
    }
