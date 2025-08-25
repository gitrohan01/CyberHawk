# parsers/wappalyzer_parser.py
from core.models import Website, ReconResult
import json

def parse(raw_output: str, website: Website, session):
    """
    Parses Wappalyzer JSON output.
    """
    try:
        data = json.loads(raw_output)
    except Exception:
        data = {"error": "Failed to parse JSON"}
    
    ReconResult.objects.create(
        session=session,
        website=website,
        tool_name="wappalyzer",
        target=website.url,
        raw_log=raw_output[:5000],
        tabular_data=data
    )
    return data
