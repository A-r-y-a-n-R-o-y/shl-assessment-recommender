import json
import pickle
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


class HybridRetriever:
    def __init__(self):
        # -----------------------------
        # Paths
        # -----------------------------
        self.catalog_path = Path("data/catalog_clean.json")
        self.bm25_path = Path("indexes/bm25.pkl")
        self.faiss_path = Path("indexes/faiss.index")

        # -----------------------------
        # Load catalog
        # -----------------------------
        print("Loading catalog...")

        with open(self.catalog_path, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

        print(f"Loaded {len(self.catalog)} assessments.")

        # -----------------------------
        # Load BM25
        # -----------------------------
        print("Loading BM25 index...")

        with open(self.bm25_path, "rb") as f:
            self.bm25 = pickle.load(f)

        print("BM25 loaded.")

        # -----------------------------
        # Load FAISS
        # -----------------------------
        print("Loading FAISS index...")

        self.index = faiss.read_index(str(self.faiss_path))

        print("FAISS loaded.")

        # -----------------------------
        # Load embedding model
        # -----------------------------
        print("Loading SentenceTransformer model...")

        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

        print("SentenceTransformer loaded.")

        print(
            f"HybridRetriever initialized with {len(self.catalog)} assessments."
        )

    def search(self, query: str, top_k: int = 10):
        """
        Hybrid search using BM25 + FAISS with Reciprocal Rank Fusion (RRF).
        """

        # -----------------------------
        # BM25 Search
        # -----------------------------
        query_tokens = query.lower().split()

        bm25_scores = self.bm25.get_scores(query_tokens)

        bm25_ranked = sorted(
            enumerate(bm25_scores),
            key=lambda x: x[1],
            reverse=True
        )[:50]

        # -----------------------------
        # Semantic Search
        # -----------------------------
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        _, faiss_indices = self.index.search(
            query_embedding,
            50
        )

        # -----------------------------
        # Reciprocal Rank Fusion
        # -----------------------------
        rrf_scores = {}
        k = 60

        for rank, (idx, _) in enumerate(bm25_ranked):
            rrf_scores[idx] = (
                rrf_scores.get(idx, 0)
                + 1 / (k + rank + 1)
            )

        for rank, idx in enumerate(faiss_indices[0]):
            rrf_scores[idx] = (
                rrf_scores.get(idx, 0)
                + 1 / (k + rank + 1)
            )

        # -----------------------------
        # Final Ranking
        # -----------------------------
        ranked = sorted(
            rrf_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for idx, score in ranked[:top_k]:

            item = self.catalog[idx]

            results.append({
                "id": item.get("id", item.get("entity_id", "")),
                "name": item.get("name", ""),
                "url": item.get("url", item.get("link", "")),
                "description": item.get("description", ""),
                "job_levels": item.get("job_levels", []),
                "categories": item.get("categories", []),
                "languages": item.get("languages", []),
                "duration": item.get("duration", ""),
                "adaptive": item.get("adaptive", ""),
                "remote": item.get("remote", ""),
                "score": round(score, 5)
            })

        return results

    def search_by_name(self, name: str):
        """
        Find the assessment whose name best matches the given name.
        """

        if not name:
            return None

        name_lower = name.lower()

        for item in self.catalog:
            if name_lower in item.get("name", "").lower():
                return {
                    "id": item.get("id", item.get("entity_id", "")),
                    "name": item.get("name", ""),
                    "url": item.get("url", item.get("link", "")),
                    "description": item.get("description", ""),
                    "job_levels": item.get("job_levels", []),
                    "categories": item.get("categories", []),
                    "languages": item.get("languages", []),
                    "duration": item.get("duration", ""),
                    "adaptive": item.get("adaptive", ""),
                    "remote": item.get("remote", ""),
                    "score": 1.0
                }

        results = self.search(name, top_k=1)

        if results:
            return results[0]

        return None