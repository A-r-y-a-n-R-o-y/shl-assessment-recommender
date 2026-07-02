import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths
DATA_FILE = Path("data/catalog_clean.json")
INDEX_DIR = Path("indexes")

EMBEDDINGS_FILE = INDEX_DIR / "embeddings.npy"
FAISS_FILE = INDEX_DIR / "faiss.index"

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# Load catalog
with open(DATA_FILE, "r", encoding="utf-8") as f:
    catalog = json.load(f)

texts = [item["search_text"] for item in catalog]

print(f"Encoding {len(texts)} assessments...")

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    normalize_embeddings=True,
    show_progress_bar=True
)

print("Embeddings shape:", embeddings.shape)

# Save embeddings
np.save(EMBEDDINGS_FILE, embeddings)

# Build FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

faiss.write_index(index, str(FAISS_FILE))

print("FAISS index created successfully.")
print(f"Saved embeddings to {EMBEDDINGS_FILE}")
print(f"Saved index to {FAISS_FILE}")