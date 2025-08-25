# parsers/retirejs_parser.py
from core.models import Website, ReconResult
import re

def parse(raw_output: str, website: Website, session):
    """
    Parse RetireJS output for vulnerable JS libraries.
    """
    lines = raw_output.splitlines()
    results = []
    for line in lines:
        if "vulnerable" in line.lower():
            results.append(line.strip())

    ReconResult.objects.create(
        session=session,
        website=website,
        tool_name="retirejs",
        target=website.url,
        raw_log=raw_output[:5000],
        tabular_data={"vulnerabilities": results}
    )
    return {"vulnerabilities": results}
