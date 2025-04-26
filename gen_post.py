#!/usr/bin/env python3
import os, requests, random
from datetime import datetime
from pytrends.request import TrendReq
import frontmatter

# 1. Scegli un topic trending
py = TrendReq(hl='it-IT', tz=360)
try:
    tr = py.trending_searches(pn='IT')
    topic = tr.sample(1).iloc[0]
except Exception as e:
    print("⚠️ PyTrends non disponibile, uso lista statica.")
    backup_keywords = [
        'tapis roulant', 'yoga a casa', 'ricette vegane',
        'videocorso fotografia', 'smartwatch economico'
    ]
    topic = random.choice(backup_keywords)

print(f"Topic scelto: {topic}")
# 2. Prepara prompt AI
prompt = (
    f"Scrivi un articolo blog SEO-friendly sul tema '{topic}'. "
    "Usa titoli H2, paragrafi brevi, includi parole chiave correlate e alla fine una call-to-action."
)

# 3. Chiamata API Hugging Face
HF_TOKEN = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {HF_TOKEN}"}
payload = {"inputs": prompt, "parameters": {"max_new_tokens": 600}}
url = "https://api-inference.huggingface.co/models/GroNLP/gpt2-medium-italian-embeddings"
res = requests.post(url, headers=headers, json=payload)
status = res.status_code
data = res.json()

if status != 200:
    print(f"❌ Errore API Hugging Face: HTTP {status}")
    print(data.get("error", data))
    exit(1)

# Se la risposta è una lista e ha il key 'generated_text'
if isinstance(data, list) and len(data) > 0 and 'generated_text' in data[0]:
    article = data[0]['generated_text']
else:
    print("❌ Risposta formato inaspettato:", data)
    exit(1)

# 4. Aggiungi link affiliato (esempio)
affiliate_link = "https://amzn.to/tuo_affiliate_code"
article += f"\n\n[Compra su Amazon!]({affiliate_link})"

# 5. Prepara front-matter e salva in _posts
date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
slug = topic.lower().replace(" ", "-")
filename = datetime.utcnow().strftime("%Y-%m-%d") + f"-{slug}.md"

metadata = {
    'title': f"I migliori consigli su {topic}",
    'date': date + " +0000",
    'tags': [topic]
}

post = frontmatter.Post(article, **metadata)
with open(f"_posts/{filename}", "w", encoding="utf-8") as f:
    frontmatter.dump(post, f)
