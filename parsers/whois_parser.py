# parsers/whois_parser.py
from core.models import Website, ReconResult
from pathlib import Path
import re
from datetime import datetime

KEYS = {
    "domain_name": re.compile(r'^\s*Domain Name:\s*(.+)\s*$', re.I),
    "registrar": re.compile(r'^\s*Registrar:\s*(.+)\s*$', re.I),
    "registrant_org": re.compile(r'^\s*Registrant Organization:\s*(.+)\s*$', re.I),
    "creation_date": re.compile(r'^\s*Creation Date:\s*(.+)\s*$', re.I),
    "updated_date": re.compile(r'^\s*Updated Date:\s*(.+)\s*$', re.I),
    "expiry_date": re.compile(r'^\s*(?:Expiry|Registry Expiry Date|Expiration Date):\s*(.+)\s*$', re.I),
    "status": re.compile(r'^\s*Domain Status:\s*(.+)\s*$', re.I),
    "name_server": re.compile(r'^\s*Name Server:\s*(.+)\s*$', re.I),
    "dnssec": re.compile(r'^\s*DNSSEC:\s*(.+)\s*$', re.I),
    "emails": re.compile(r'[\w\.-]+@[\w\.-]+\.\w+'),
}

def _parse_date(s):
    # handle common whois date variants
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S%z", "%Y-%m-%d", "%d-%b-%Y"):
        try:
            return datetime.strptime(s.strip(), fmt).iso8601()  # will raise on older python; fallback below
        except Exception:
            pass
    try:
        return datetime.fromisoformat(s.strip().replace("Z", "+00:00")).isoformat()
    except Exception:
        return s.strip()

def parse_whois_file(domain_name: str):
    path = Path(f"reports/info_gathering/whois/{domain_name}_whois.txt")
    if not path.exists():
        print(f"[whois] file not found: {path}")
        return

    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    website, _ = Website.objects.get_or_create(url=domain_name)

    domain = registrar = registrant_org = dnssec = None
    creation_date = updated_date = expiry_date = None
    statuses, nameservers, emails = [], [], set()

    for line in lines:
        s = line.strip()
        if not s or s.startswith('%') or s.startswith('#'):
            continue

        m = KEYS["domain_name"].match(s)
        if m: domain = m.group(1).strip().lower().rstrip('.'); continue

        m = KEYS["registrar"].match(s)
        if m: registrar = m.group(1).strip(); continue

        m = KEYS["registrant_org"].match(s)
        if m: registrant_org = m.group(1).strip(); continue

        m = KEYS["creation_date"].match(s)
        if m: creation_date = _parse_date(m.group(1)); continue

        m = KEYS["updated_date"].match(s)
        if m: updated_date = _parse_date(m.group(1)); continue

        m = KEYS["expiry_date"].match(s)
        if m: expiry_date = _parse_date(m.group(1)); continue

        m = KEYS["status"].match(s)
        if m: statuses.append(m.group(1).strip()); continue

        m = KEYS["name_server"].match(s)
        if m: nameservers.append(m.group(1).strip().rstrip('.').lower()); continue

        for e in KEYS["emails"].findall(s):
            emails.add(e.lower())

    tabular = {
        "domain": domain or domain_name.lower(),
        "registrar": registrar,
        "registrant_org": registrant_org,
        "creation_date": creation_date,
        "updated_date": updated_date,
        "expiry_date": expiry_date,
        "statuses": sorted(set(statuses)),
        "name_servers": sorted(set(nameservers)),
        "emails": sorted(emails),
        "dnssec": dnssec,
    }
    raw_log = {"raw": text[:8000]}

    ToolResult.objects.create(
        website=website,
        tool_name="whois",
        target=domain_name,
        tabular_data=tabular,
        raw_log=raw_log
    )
    print(f"[whois] parsed & saved for {domain_name}")
