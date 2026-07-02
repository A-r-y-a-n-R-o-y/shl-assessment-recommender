import json
import pickle
from rank_bm25 import BM25Okapi

# Load cleaned catalog
with open("data/catalog_clean.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Tokenize each assessment
corpus = [
    item["search_text"].lower().split()
    for item in catalog
]

bm25 = BM25Okapi(corpus)

with open("indexes/bm25.pkl", "wb") as f:
    pickle.dump(bm25, f)

print(f"BM25 index built for {len(catalog)} assessments.")