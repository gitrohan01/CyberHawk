# parsers/httpx_parser.py
from core.models import Website, ReconResult

def parse(raw_output: str, website: Website, session):
    """
    Parses httpx output like URL, status, title, technologies.
    """
    lines = raw_output.splitlines()
    results = []
    for line in lines:
        if line.strip():
            # Example: http://example.com [200 OK] Title: Example
            parts = line.split()
            url = parts[0]
            status = parts[1] if len(parts) > 1 else ""
            title = " ".join(parts[2:]).replace("Title:", "").strip() if len(parts) > 2 else ""
            results.append({"url": url, "status": status, "title": title})

    ReconResult.objects.create(
        session=session,
        website=website,
        tool_name="httpx",
        target=website.url,
        raw_log=raw_output[:5000],
        tabular_data={"results": results}
    )

    return {"results": results}
