import os
import sys
import django

# Setup Django so parsers can use core.models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cyberhawk.settings")
django.setup()

from parsers import (
    dig_parser,
    host_parser,
    nslookup_parser,
    ping_parser,
    traceroute_parser,
    whois_parser,
    httpx_parser,
    whatweb_parser,
    wappalyzer_parser,
    cmseek_parser,
    retirejs_parser,
    wpscan_parser,
    
)


TOOLS = {
    "dig": dig_parser.parse_dig_file,
    "host": host_parser.parse_host_file,
    "nslookup": nslookup_parser.parse_nslookup_file,
    "ping": ping_parser.parse_ping_file,
    "traceroute": traceroute_parser.parse_traceroute_file,
    "whois": whois_parser.parse_whois_file,
    "httpx": httpx_parser.parse_httpx_file,
    "whatweb": whatweb_parser.parse_whatweb_file,
    "wappalyzer": wappalyzer_parser.parse_wappalyzer_file,
    "cmseek": cmseek_parser.parse_cmseek_file,
    "retirejs": retirejs_parser.parse_retirejs_file,
    "wpscan": wpscan_parser.parse_wpscan_file,
    
}

def run_parsers(domain_name: str, session_id: int = None, tool: str = None):
    """
    Run parsers for a single domain.
    If tool is specified, only that parser is run.
    Otherwise all available parsers are tried.
    """
    if tool:
        parser = TOOLS.get(tool)
        if parser:
            if tool == "dig":
                parser(domain_name, session_id)
            else:
                parser(domain_name)
        else:
            print(f"[!] No parser for tool: {tool}")
    else:
        for t, parser in TOOLS.items():
            try:
                if t == "dig":
                    parser(domain_name, session_id)
                else:
                    parser(domain_name)
            except Exception as e:
                print(f"[{t}] error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <domain> [session_id] [tool]")
        sys.exit(1)

    domain = sys.argv[1]
    session = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else None
    tool = sys.argv[3] if len(sys.argv) > 3 else None

    run_parsers(domain, session, tool)
