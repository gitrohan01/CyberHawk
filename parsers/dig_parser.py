# parsers/dig_parser.py
from core.models import Website, DigRecord, ReconResult, ScanSession
from pathlib import Path
import re

def parse_dig_file(domain_name: str, session_id: int):
    file_path = Path(f"reports/info_gathering/dig/{domain_name}_dig.txt")
    if not file_path.exists():
        print(f"[dig] file not found: {file_path}")
        return

    text = file_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    # Link to ScanSession
    try:
        session = ScanSession.objects.get(id=session_id)
    except ScanSession.DoesNotExist:
        print(f"[dig] session {session_id} not found")
        return

    # Get or create Website
    website_obj, _ = Website.objects.get_or_create(url=domain_name)

    # Clean old dig records for this website (avoid dupes)
    website_obj.dig_records.all().delete()

    # Extract Answer Section
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

        # Save to DigRecord table
        try:
            DigRecord.objects.create(
                website=website_obj,
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

    # Save into ReconResult
    ReconResult.objects.create(
        session=session,
        tool_name="dig",
        output=text[:2000],  # keep raw log truncated
        structured_data={"records": records}
    )

    print(f"[dig] parsed & saved for {domain_name} in session {session_id}")
