# parsers/host_parser.py
from core.models import Website, ReconResult
from pathlib import Path
import re

def parse_host_file(domain_name: str):
    path = Path(f"reports/info_gathering/host/{domain_name}_host.txt")
    if not path.exists():
        print(f"[host] file not found: {path}")
        return

    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    website, _ = Website.objects.get_or_create(url=domain_name)

    # host outputs lines like:
    # example.com has address 93.184.216.34
    # example.com has IPv6 address 2606:2800:220:1:248:1893:25c8:1946
    # example.com mail is handled by 10 mx1.example.com.
    # example.com is an alias for www.example.com.
    A, AAAA, MX, CNAME, NS, TXT = [], [], [], [], [], []

    mx_re = re.compile(r"mail is handled by\s+(\d+)\s+(\S+)")
    a_re = " has address "
    aaaa_re = " has IPv6 address "
    cname_re = " is an alias for "
    ns_re = re.compile(r" name server (\S+)")
    txt_re = re.compile(r' descriptive text "(.*)"')

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if a_re in line:
            A.append(line.split(a_re, 1)[1].strip().rstrip('.'))
        elif aaaa_re in line:
            AAAA.append(line.split(aaaa_re, 1)[1].strip().rstrip('.'))
        else:
            m = mx_re.search(line)
            if m:
                MX.append({"priority": int(m.group(1)), "host": m.group(2).rstrip('.')})
                continue
            m = ns_re.search(line)
            if m:
                NS.append(m.group(1).rstrip('.'))
                continue
            m = cname_re in line and line.split(cname_re, 1)[1].strip()
            if m:
                CNAME.append(str(m).rstrip('.'))
                continue
            m = txt_re.search(line)
            if m:
                TXT.append(m.group(1))

    tabular = {
        "A": sorted(set(A)),
        "AAAA": sorted(set(AAAA)),
        "CNAME": sorted(set(CNAME)),
        "MX": sorted(MX, key=lambda x: x["priority"]) if MX else [],
        "NS": sorted(set(NS)),
        "TXT": TXT,
    }

    raw_log = {
        "raw": text[:4000]  # bounded
    }

    ReconResult.objects.create(
        website=website,
        tool_name="host",
        target=domain_name,
        tabular_data=tabular,
        raw_log=raw_log
    )
    print(f"[host] parsed & saved for {domain_name}")
