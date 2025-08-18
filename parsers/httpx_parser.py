from core.models import Website, ReconResult
from pathlib import Path
import json

def parse_httpx_file(domain_name: str):
    path = Path(f"reports/info_gathering/httpx/{domain_name}_httpx.json")
    if not path.exists():
        print(f"[httpx] file not found: {path}")
        return

    text = path.read_text(encoding="utf-8", errors="ignore")
    website, _ = Website.objects.get_or_create(url=domain_name)

    structured = []
    for line in text.strip().splitlines():
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        structured.append({
            "url": data.get("url"),
            "status": data.get("status-code"),
            "title": data.get("title"),
            "ip": data.get("host"),
            "tech": data.get("tech", [])
        })

    ReconResult.objects.create(
        website=website,
        tool_name="httpx",
        target=domain_name,
        structured_data={"results": structured},
        raw_log={"raw": text[:4000]}
    )
    print(f"[httpx] parsed & saved for {domain_name}")
