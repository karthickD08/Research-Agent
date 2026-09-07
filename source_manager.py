from urllib.parse import urlsplit, urlunsplit


def normalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), "", ""))


def source_quality(url: str) -> float:
    host = urlsplit(url).netloc.lower()
    if host.endswith(".gov") or host.endswith(".gov.in"):
        return 0.95
    if host.endswith(".edu"):
        return 0.92
    if any(host.endswith(x) for x in [".ac.uk", ".ac.in", ".edu.au"]):
        return 0.92
    if any(domain in host for domain in ["nature.com", "science.org", "ieee.org", "arxiv.org"]):
        return 0.90
    if any(domain in host for domain in ["reuters.com", "apnews.com", "bbc.com"]):
        return 0.85
    return 0.65


def deduplicate_sources(raw_sources: list[dict]) -> list[dict]:
    seen = set()
    unique = []

    for source in raw_sources:
        url = source.get("url", "")
        if not url:
            continue

        key = normalize_url(url)
        if key in seen:
            continue

        seen.add(key)
        source = dict(source)
        source["url"] = url
        source["quality"] = source_quality(url)
        unique.append(source)

    unique.sort(key=lambda x: (x.get("quality", 0), x.get("score", 0)), reverse=True)

    numbered = []
    for index, source in enumerate(unique, start=1):
        source["id"] = f"S{index}"
        numbered.append(source)

    return numbered


def source_context(sources: list[dict]) -> str:
    chunks = []
    for s in sources:
        chunks.append(
            f"[{s['id']}] {s['title']}\n"
            f"URL: {s['url']}\n"
            f"Search relevance: {s.get('score', 0):.2f}\n"
            f"Quality estimate: {s.get('quality', 0):.2f}\n"
            f"Content: {s.get('content', '')[:2500]}"
        )
    return "\n\n".join(chunks)
