# parsers/whatweb_parser.py
from core.models import Website, ReconResult
import re

def parse(raw_output: str, website: Website, session):
    """
    Parse WhatWeb output.
    """
    lines = raw_output.splitlines()
    plugins = []
    for line in lines:
        if line.strip():
            plugins.append(line.strip())

    ReconResult.objects.create(
        session=session,
        website=website,
        tool_name="whatweb",
        target=website.url,
        raw_log=raw_output[:5000],
        tabular_data={"plugins": plugins}
    )
    return {"plugins": plugins}
