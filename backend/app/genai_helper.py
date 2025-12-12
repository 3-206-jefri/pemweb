import os
import json
import google.generativeai as genai

# Load API KEY
GEN_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEN_API_KEY)

# Pakai model terbaru (lebih murah & cepat)
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_key_points(text, max_points=5):
    prompt = (
        f"Extract up to {max_points} key points from this product review.\n"
        f"Return ONLY a JSON array of short bullet points.\n\n"
        f"Review:\n{text}"
    )

    try:
        response = model.generate_content(prompt)
        content = response.text.strip()
        # coba parse sebagai JSON
        try:
            parsed = json.loads(content)
            return parsed
        except Exception:
            lines = [l.strip(" -•\t") for l in content.splitlines() if l.strip()]
            return lines[:max_points]
    except Exception:
        # fallback simple extraction if Gemini API is not available
        sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
        # return up to max_points short sentence fragments
        return sentences[:max_points]
