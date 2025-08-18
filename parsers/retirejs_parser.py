from core.models import Website, ReconResult
from pathlib import Path
import json

def parse_retirejs_file(domain_name: str):
    path = Path(f"reports/info_gathering/retirejs/{domain_name}_retirejs.json")
    if not path.exists():
        print(f"[retirejs] file not found: {path}")
        return

    text = path.read_text(encoding="utf-8", errors="ignore")
    website, _ = Website.objects.get_or_create(url=domain_name)

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        print("[retirejs] invalid JSON")
        return

    ReconResult.objects.create(
        website=website,
        tool_name="retirejs",
        target=domain_name,
        structured_data=data,
        raw_log={"raw": text[:4000]}
    )
    print(f"[retirejs] parsed & saved for {domain_name}")
