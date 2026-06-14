import arxiv

# TESTED OK
def search_paper(query: str):
    try:
        client = arxiv.Client(
            page_size=5,
            delay_seconds=3,
            num_retries=5
        )

        search = arxiv.Search(
            query=query,
            max_results=5
        )

        papers = []

        for paper in client.results(search):
            papers.append({
                "title": paper.title,
                "summary": paper.summary,
                "url": paper.entry_id
            })

        return papers

    except Exception as e:
        print(f"Error: {e}")
        return []
# print(search_paper("quantum computing"))