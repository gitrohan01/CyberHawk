# parsers/cmseek_parser.py
from core.models import Website, ReconResult

def parse(raw_output: str, website: Website, session):
    """
    Parses CMSeek output for services, version, ports.
    """
    lines = raw_output.splitlines()
    results = []

    for line in lines:
        if line.strip() and ":" in line:
            # Example: http:80 Apache/2.4.41
            parts = line.split(":", 1)
            service_port = parts[0].strip()
            service_info = parts[1].strip()
            results.append({"service_port": service_port, "service_info": service_info})

    ReconResult.objects.create(
        session=session,
        website=website,
        tool_name="cmseek",
        target=website.url,
        raw_log=raw_output[:5000],
        tabular_data={"services": results}
    )

    return {"services": results}
