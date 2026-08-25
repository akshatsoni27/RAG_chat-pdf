import arxiv

client = arxiv.Client()

search = arxiv.Search(
    query="large language models",
    max_results=2,
    sort_by=arxiv.SortCriterion.Relevance
)

results = client.results(search)

for i, result in enumerate(results):
    print(f"\nResult {i + 1}")
    print("Title:", result.title)
    print("Authors:", ", ".join(author.name for author in result.authors))
    print("Summary:", result.summary)
    print("URL:", result.entry_id)