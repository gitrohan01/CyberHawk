# parsers/traceroute_parser.py
from core.models import Website, ReconResult
import re

def parse(raw_output: str, website: Website, session):
    lines = raw_output.splitlines()
    hops = []

    hop_re = re.compile(r"(\d+)\s+([\d\.\*]+)\s+.*")

    for line in lines:
        m = hop_re.match(line)
        if m:
            hop_num = int(m.group(1))
            ip = m.group(2)
            hops.append({"hop": hop_num, "ip": ip})

    ReconResult.objects.create(
        session=session,
        website=website,
        tool_name="traceroute",
        target=website.url,
        raw_log=raw_output[:5000],
        tabular_data={"hops": hops}
    )
    return {"hops": hops}
