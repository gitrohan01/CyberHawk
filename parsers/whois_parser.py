# parsers/whois_parser.py
from core.models import Website, ReconResult

def parse(raw_output: str, website: Website, session):
    """
    Parse WHOIS output into structured dict by line.
    """
    lines = raw_output.splitlines()
    whois_data = {}
    for line in lines:
        if ":" in line:
            k, v = line.split(":", 1)
            whois_data[k.strip()] = v.strip()

    ReconResult.objects.create(
        session=session,
        website=website,
        tool_name="whois",
        target=website.url,
        raw_log=raw_output[:5000],
        tabular_data=whois_data
    )
    return whois_data
