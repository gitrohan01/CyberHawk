from core.models import Website, ReconResult
from pathlib import Path
import re

def parse_blindelephant_file(domain_name: str):
    path = Path(f"reports/info_gathering/blindelephant/{domain_name}_blindelephant.txt")
    if not path.exists():
        print(f"[blindelephant] file not found: {path}")
        return

    text = path.read_text(encoding="utf-8", errors="ignore")
    website, _ = Website.objects.get_or_create(url=domain_name)

    # BlindElephant output usually contains lines like:
    # [+] Fingerprinting Joomla...
    # [+] Version identified: 3.9.16
    version = None
    m = re.search(r"Version identified:\s*([\d\.]+)", text)
    if m:
        version = m.group(1)

    structured = {"version": version} if version else {}

    ReconResult.objects.create(
        website=website,
        tool_name="blindelephant",
        target=domain_name,
        structured_data=structured,
        raw_log={"raw": text[:4000]}
    )
    print(f"[blindelephant] parsed & saved for {domain_name}")
