# parsers/host_parser.py
from core.models import Website, ReconResult, ScanSession

import re

def parse(raw_output: str, website: Website, session: ScanSession):
    lines = raw_output.splitlines()

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
            if cname_re in line:
                CNAME.append(line.split(cname_re, 1)[1].strip().rstrip('.'))
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
        "TXT": TXT
    }

    ReconResult.objects.create(
        session=session,
        website=website,
        tool_name="host",
        target=website.url,
        raw_log=raw_output[:5000],
        tabular_data=tabular
    )

    return tabular
