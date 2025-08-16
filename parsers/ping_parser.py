# parsers/ping_parser.py
from core.models import Website, ReconResult
from pathlib import Path
import re
import statistics

def parse_ping_file(domain_name: str):
    path = Path(f"reports/info_gathering/ping/{domain_name}_ping.txt")
    if not path.exists():
        print(f"[ping] file not found: {path}")
        return

    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    website, _ = Website.objects.get_or_create(url=domain_name)

    # Linux ping summary lines look like:
    # --- example.com ping statistics ---
    # 5 packets transmitted, 5 received, 0% packet loss, time 4006ms
    # rtt min/avg/max/mdev = 13.092/15.002/17.219/1.384 ms
    tx = rx = loss = None
    rtt_min = rtt_avg = rtt_max = rtt_mdev = None
    samples = []

    ttl_re = re.compile(r'ttl=(\d+)')
    time_re = re.compile(r'time=([\d\.]+)\s*ms')
    stats_re = re.compile(r'(\d+)\s+packets transmitted,\s+(\d+)\s+received,\s+([\d\.]+)%\s+packet loss')
    rtt_re = re.compile(r'rtt min/avg/max/(?:mdev|stddev)\s*=\s*([\d\.]+)/([\d\.]+)/([\d\.]+)/([\d\.]+)\s*ms')

    for line in lines:
        m = time_re.search(line)
        if m:
            try:
                samples.append(float(m.group(1)))
            except Exception:
                pass

        m = stats_re.search(line)
        if m:
            tx = int(m.group(1)); rx = int(m.group(2)); loss = float(m.group(3))

        m = rtt_re.search(line)
        if m:
            rtt_min, rtt_avg, rtt_max, rtt_mdev = map(float, m.groups())

    # Fallback average if summary missing
    if samples and rtt_avg is None:
        rtt_avg = statistics.mean(samples)

    tabular = {
        "transmitted": tx,
        "received": rx,
        "packet_loss_percent": loss,
        "rtt_min_ms": rtt_min,
        "rtt_avg_ms": rtt_avg,
        "rtt_max_ms": rtt_max,
        "rtt_mdev_ms": rtt_mdev,
        "samples_count": len(samples)
    }
    raw_log = {
        "samples_ms": samples[:200],  # bounded list
        "raw": text[:4000]
    }

    ReconResult.objects.create(
        website=website,
        tool_name="ping",
        target=domain_name,
        tabular_data=tabular,
        raw_log=raw_log
    )
    print(f"[ping] parsed & saved for {domain_name}")
