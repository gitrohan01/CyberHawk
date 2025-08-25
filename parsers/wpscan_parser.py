# parsers/wpscan_parser.py
from core.models import Website, ReconResult
import re

def parse(raw_output: str, website: Website, session):
    """
    Parses WPScan output for vulnerabilities and plugins.
    """
    lines = raw_output.splitlines()
    vulns = []
    plugins = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "vulnerability" in line.lower():
            vulns.append(line)
        elif "Plugin:" in line:
            plugins.append(line.replace("Plugin:", "").strip())

    tabular_data = {
        "vulnerabilities": vulns,
        "plugins": plugins
    }

    ReconResult.objects.create(
        session=session,
        website=website,
        tool_name="wpscan",
        target=website.url,
        raw_log=raw_output[:5000],
        tabular_data=tabular_data
    )
    return tabular_data
