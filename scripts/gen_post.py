from pytrends.request import TrendReq
py = TrendReq(hl='it-IT', tz=360)
trending = py.trending_searches(pn='IA')  # parole chiave calde in Italia
topic = trending.iloc[0]  # prendi il primo trend

import os, requests
HF_TOKEN = os.getenv("HF_TOKEN")  # metti il tuo token HuggingFace come segreto
headers = {"Authorization": f"Bearer {HF_TOKEN}"}
prompt = (f"Scrivi un articolo di blog informativo ed SEO-friendly sul tema '{topic}'. "
          "Dividilo in paragrafi con sottotitoli H2, includi parole chiave correlate e termini come '" +
          topic + "', 'migliori', '2025'. Alla fine aggiungi una call-to-action per un prodotto pertinente.")
payload = {"inputs": prompt, "parameters": {"max_new_tokens": 600}}
url = "https://api-inference.huggingface.co/models/GroNLP/gpt2-medium-italian-embeddings"
res = requests.post(url, headers=headers, json=payload)
article = res.json()[0]['generated_text']
