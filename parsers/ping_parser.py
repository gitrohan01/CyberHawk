# parsers/ping_parser.py
from core.models import Website, ReconResult
import re

def parse(raw_output: str, website: Website, session):
    lines = raw_output.splitlines()
    stats = {}
    for line in lines:
        if "packets transmitted" in line:
            stats["summary"] = line.strip()
        elif "min/avg/max" in line or "rtt" in line:
            stats["rtt"] = line.strip()

    ReconResult.objects.create(
        session=session,
        website=website,
        tool_name="ping",
        target=website.url,
        raw_log=raw_output[:5000],
        tabular_data=stats
    )
    return stats
