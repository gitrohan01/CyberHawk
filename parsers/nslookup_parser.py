# parsers/nslookup_parser.py
from core.models import Website, ReconResult
import re

def parse(raw_output: str, website: Website, session):
    lines = raw_output.splitlines()
    records = []

    for line in lines:
        if "Name:" in line or "Address:" in line:
            records.append(line.strip())

    ReconResult.objects.create(
        session=session,
        website=website,
        tool_name="nslookup",
        target=website.url,
        raw_log=raw_output[:5000],
        tabular_data={"records": records}
    )
    return {"records": records}
