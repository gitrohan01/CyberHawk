# parsers/dig_parser.py
from core.models import Website, DigRecord, ReconResult, ScanSession
import re

def parse(raw_output: str, website: Website, session: ScanSession):
    """
    Parses dig output from raw string and stores records in DB.
    Returns structured data as dict.
    """
    lines = raw_output.splitlines()

    # Clean old dig records
    website.dig_records.all().delete()

    answer_section = []
    section = None
    for line in lines:
        if line.startswith(';; ANSWER SECTION:'):
            section = 'answer'
            continue
        elif line.startswith(';;') and section == 'answer':
            break
        if section == 'answer' and line.strip() and not line.startswith(';'):
            answer_section.append(line.strip())

    records = []
    for rec in answer_section:
        parts = rec.split()
        if len(parts) < 5:
            continue
        name, ttl, cls, rtype = parts[0], parts[1], parts[2], parts[3]
        rdata = ' '.join(parts[4:])
        mx_priority = None

        if rtype == 'MX':
            mx_match = re.match(r'(\d+)\s+(.*)', rdata)
            if mx_match:
                mx_priority = int(mx_match.group(1))
                rdata = mx_match.group(2)

        try:
            DigRecord.objects.create(
                website=website,
                record_type=rtype,
                ttl=int(ttl) if ttl.isdigit() else None,
                record_name=name,
                record_data=rdata,
                mx_priority=mx_priority
            )
        except Exception as e:
            print(f"[dig] record save error: {e}")

        records.append({
            "name": name.rstrip('.'),
            "ttl": int(ttl) if ttl.isdigit() else ttl,
            "class": cls,
            "type": rtype,
            "data": rdata.rstrip('.'),
            "mx_priority": mx_priority
        })

    # Save ReconResult
    ReconResult.objects.create(
        session=session,
        website=website,
        tool_name="dig",
        target=website.url,
        raw_log=raw_output[:5000],
        tabular_data={"records": records}
    )

    return {"records": records}
