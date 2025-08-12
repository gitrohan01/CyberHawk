from core.models import Website, DigRecord
import re

def parse_dig_file(domain_name):
    file_path = f'reports/info_gathering/dig/{domain_name}_dig.txt'

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Get or create Website object
    website_obj, _ = Website.objects.get_or_create(url=domain_name)

    # Clear old dig records to avoid duplicates
    website_obj.dig_records.all().delete()

    section = None
    answer_section = []

    for line in lines:
        if line.startswith(';; ANSWER SECTION:'):
            section = 'answer'
            continue
        elif line.startswith(';;') and section == 'answer':
            # End of ANSWER section when another section or comment starts
            break

        if section == 'answer':
            answer_section.append(line.strip())

    # Parse each line in ANSWER SECTION
    for record_line in answer_section:
        if not record_line or record_line.startswith(';'):
            continue

        # Expected format: name, ttl, class, type, data
        parts = record_line.split()
        if len(parts) < 5:
            continue

        name, ttl, cls, rtype = parts[0], parts[1], parts[2], parts[3]
        rdata = ' '.join(parts[4:])

        mx_priority = None
        if rtype == 'MX':
            # MX records have priority and domain e.g. "10 mail.example.com."
            mx_match = re.match(r'(\d+)\s+(.*)', rdata)
            if mx_match:
                mx_priority = int(mx_match.group(1))
                rdata = mx_match.group(2)

        DigRecord.objects.create(
            website=website_obj,
            record_type=rtype,
            ttl=int(ttl),
            record_name=name,
            record_data=rdata,
            mx_priority=mx_priority
        )

    print(f'Parsed dig file and saved records for domain: {domain_name}')
