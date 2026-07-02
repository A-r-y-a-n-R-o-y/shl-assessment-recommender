import json
from pathlib import Path

INPUT_FILE = Path("data/catalog.json")
OUTPUT_FILE = Path("data/catalog_clean.json")


def clean_text(text):
    """Normalize whitespace."""
    if not text:
        return ""

    return " ".join(str(text).split())


def build_search_text(item):
    parts = [
        item.get("name", ""),
        item.get("description", ""),
        " ".join(item.get("job_levels", [])),
        " ".join(item.get("keys", [])),
        " ".join(item.get("languages", [])),
        item.get("duration", ""),
        item.get("adaptive", ""),
        item.get("remote", "")
    ]

    return clean_text(" ".join(parts))


def preprocess():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    cleaned = []

    for item in catalog:

        record = {
            "id": item["entity_id"],
            "name": clean_text(item["name"]),
            "description": clean_text(item["description"]),
            "url": item["link"],
            "job_levels": item["job_levels"],
            "categories": item["keys"],
            "languages": item["languages"],
            "duration": clean_text(item["duration"]),
            "adaptive": item["adaptive"],
            "remote": item["remote"],
            "search_text": build_search_text(item)
        }

        cleaned.append(record)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(cleaned)} assessments.")


if __name__ == "__main__":
    preprocess()