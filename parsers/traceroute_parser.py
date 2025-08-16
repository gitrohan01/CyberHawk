# parsers/traceroute_parser.py
from core.models import Website, ReconResult
from pathlib import Path
import re

def parse_traceroute_file(domain_name: str):
    path = Path(f"reports/info_gathering/traceroute/{domain_name}_traceroute.txt")
    if not path.exists():
        print(f"[traceroute] file not found: {path}")
        return

    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    website, _ = Website.objects.get_or_create(url=domain_name)

    # Typical line:
    #  1  router.lan (192.168.1.1)  2.123 ms  1.876 ms  1.654 ms
    hop_re = re.compile(
        r'^\s*(\d+)\s+([^\s(]+)?\s*(?:\(([^)]+)\))?\s+([\d\.\s]+)ms'
    )
    time_re = re.compile(r'(\d+\.\d+)\s*ms')
    star_re = re.compile(r'\*')

    hops = []
    for line in lines:
        if not line.strip():
            continue
        # collect times even if stars present
        times = [float(t) for t in time_re.findall(line)]
        stars = len(star_re.findall(line))
        m = re.match(r'^\s*(\d+)\s+(.+)$', line)
        if not m:
            continue
        hop_no = int(m.group(1))
        rest = m.group(2)

        host = None
        ip = None
        m2 = re.search(r'([^\s(]+)\s+\(([^)]+)\)', rest)
        if m2:
            host = m2.group(1)
            ip = m2.group(2)
        else:
            # sometimes only IP appears
            m3 = re.search(r'\(([^)]+)\)', rest)
            if m3:
                ip = m3.group(1)
            else:
                # or just a hostname
                m4 = re.match(r'([^\s]+)', rest)
                host = m4.group(1) if m4 else None

        hops.append({
            "hop": hop_no,
            "host": host,
            "ip": ip,
            "rtt_ms": times,
            "timeouts": stars
        })

    tabular = {"hops": hops}
    raw_log = {"raw": text[:6000]}

    ReconResult.objects.create(
        website=website,
        tool_name="traceroute",
        target=domain_name,
        tabular_data=tabular,
        raw_log=raw_log
    )
    print(f"[traceroute] parsed & saved for {domain_name}")
