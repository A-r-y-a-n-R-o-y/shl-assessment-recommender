from app.retrieval import HybridRetriever

retriever = HybridRetriever()

results = retriever.search(
    "Java developer with stakeholder communication",
    top_k=10
)

print(f"\nFound {len(results)} results:\n")

for i, result in enumerate(results, start=1):
    print("=" * 70)
    print(f"{i}. {result['name']}")
    print(f"Score: {result['score']}")
    print(f"Categories: {', '.join(result['categories'])}")
    print(f"Job Levels: {', '.join(result['job_levels'])}")
    print(f"URL: {result['url']}")