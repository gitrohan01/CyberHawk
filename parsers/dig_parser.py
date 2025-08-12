import re
from core.models import Domain, DigRecord

def parse_dig_file(domain_name):
    file_path = f'/app/reports/info_gathering/dig/{domain_name}_dig.txt'

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Create or get Domain object
    domain_obj, _ = Domain.objects.get_or_create(name=domain_name)

    # Clear old records for fresh import (optional)
    domain_obj.dig_records.all().delete()

    section = None
    answer_section = []
    for line in lines:
        if line.startswith(';; ANSWER SECTION:'):
            section = 'answer'
            continue
        elif line.startswith(';;') and section == 'answer':
            # End of ANSWER section
            break
        if section == 'answer':
            answer_section.append(line.strip())

    # Parse each record line in ANSWER SECTION
    for record_line in answer_section:
        if not record_line or record_line.startswith(';'):
            continue
        # Example: example.com. 299 IN A 93.184.216.34
        parts = record_line.split()
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

        DigRecord.objects.create(
            domain=domain_obj,
            record_type=rtype,
            ttl=int(ttl),
            record_name=name,
            record_data=rdata,
            mx_priority=mx_priority
        )

    print(f'Parsed dig file and saved records for domain: {domain_name}')
