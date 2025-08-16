# parsers/nslookup_parser.py
from core.models import Website, ReconResult
from pathlib import Path
import re

def parse_nslookup_file(domain_name: str):
    path = Path(f"reports/info_gathering/nslookup/{domain_name}_nslookup.txt")
    if not path.exists():
        print(f"[nslookup] file not found: {path}")
        return

    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    website, _ = Website.objects.get_or_create(url=domain_name)

    A, AAAA, CNAME, NS, MX, TXT = [], [], [], [], [], []
    current_section = None
    # Common patterns
    a_re = re.compile(r"Address:\s*([\d.]+)$")
    a_alt_re = re.compile(r"Addresses:\s*(.+)$")
    aaaa_re = re.compile(r"Address:\s*([0-9a-fA-F:]+)$")
    cname_re = re.compile(r"canonical name\s*=\s*(\S+)")
    ns_re = re.compile(r"nameserver\s*=\s*(\S+)")
    mx_re = re.compile(r"mail exchanger\s*=\s*(\S+)")
    mx_prio_re = re.compile(r"preference\s*=\s*(\d+),\s*mail exchanger\s*=\s*(\S+)")
    txt_re = re.compile(r'Text\s*=\s*"(.*)"')

    for line in lines:
        s = line.strip()
        if not s:
            continue

        # Sections
        if s.lower().startswith("non-authoritative answer"):
            current_section = "answer"
            continue
        if s.lower().startswith("authoritative answers"):
            current_section = "authoritative"
            continue

        # Matches
        m = cname_re.search(s)
        if m:
            CNAME.append(m.group(1).rstrip('.'))
            continue

        m = ns_re.search(s)
        if m:
            NS.append(m.group(1).rstrip('.'))
            continue

        m = mx_prio_re.search(s) or mx_re.search(s)
        if m:
            if m.re is mx_prio_re:
                MX.append({"priority": int(m.group(1)), "host": m.group(2).rstrip('.')})
            else:
                MX.append({"priority": None, "host": m.group(1).rstrip('.')})
            continue

        m = txt_re.search(s)
        if m:
            TXT.append(m.group(1))
            continue

        # Address variants (IPv4/IPv6)
        m = a_re.search(s)
        if m:
            A.append(m.group(1))
            continue
        m = aaaa_re.search(s)
        if m:
            AAAA.append(m.group(1))
            continue
        m = a_alt_re.search(s)
        if m:
            # could be comma-separated
            for addr in m.group(1).split():
                addr = addr.strip().strip(',')
                if ':' in addr:
                    AAAA.append(addr)
                elif re.match(r'^\d+\.\d+\.\d+\.\d+$', addr):
                    A.append(addr)

    tabular = {
        "A": sorted(set(A)),
        "AAAA": sorted(set(AAAA)),
        "CNAME": sorted(set(CNAME)),
        "NS": sorted(set(NS)),
        "MX": sorted([mx for mx in MX if mx.get("host")], key=lambda x: (x["priority"] or 9999, x["host"])) if MX else [],
        "TXT": TXT
    }
    raw_log = {"raw": text[:4000]}

    ToolResult.objects.create(
        website=website,
        tool_name="nslookup",
        target=domain_name,
        tabular_data=tabular,
        raw_log=raw_log
    )
    print(f"[nslookup] parsed & saved for {domain_name}")
