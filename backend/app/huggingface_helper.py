import os, requests
HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")
HUGGINGFACE_MODEL = os.environ.get("HUGGINGFACE_MODEL", "cardiffnlp/twitter-roberta-base-sentiment")

HF_API = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"

def analyze_sentiment(text):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
    payload = {"inputs": text}
    try:
        resp = requests.post(HF_API, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        # response format varies by model; adjust parsing accordingly
        if isinstance(data, list) and data:
            top = max(data, key=lambda x: x.get('score', 0))
            return top.get('label', 'neutral')
        return str(data)
    except Exception:
        # fallback simple heuristic when HF API is unavailable or model removed
        text_lower = text.lower()
        positive_words = ['bagus', 'baik', 'love', 'great', 'mantap', 'recommended', 'recommend']
        negative_words = ['buruk', 'jelek', 'tidak', 'boros', 'hate', 'bad']
        score = 0
        for w in positive_words:
            if w in text_lower:
                score += 1
        for w in negative_words:
            if w in text_lower:
                score -= 1
        if score > 0:
            return 'positive'
        if score < 0:
            return 'negative'
        return 'neutral'
