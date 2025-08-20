import subprocess
import os
from datetime import datetime

# Base paths
TOOLS_DIR = "./info_gathering"  # Where the tool folders like blindelephant, dig, etc. exist
REPORTS_DIR = "./reports/info_gathering"


# Tools and their folders
TOOLS = [
    "blindelephant",
    "cmseek",
    "dig",
    "host",
    "httpx",
    "nslookup",
    "ping",
    "retirejs",
    "traceroute",
    "wappalyzer",
    "whatweb",
    "whois",
    "wpscan"
]

TARGET = input("Enter target domain/IP/URL: ")

def run_tool(tool_name):
    tool_path = os.path.join(TOOLS_DIR, tool_name)
    run_sh = os.path.join(tool_path, "run.sh")
    
    if os.path.isfile(run_sh):
        print(f"[+] Running {tool_name}...")
        try:
            subprocess.run(["bash", run_sh, TARGET], check=True)  # pass TARGET here
            print(f"[+] {tool_name} completed.")
        except subprocess.CalledProcessError as e:
            print(f"[!] {tool_name} failed: {e}")
    else:
        print(f"[!] No run.sh found for {tool_name}, skipping.")

def ensure_report_dirs():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
    for tool in TOOLS:
        path = os.path.join(REPORTS_DIR, tool)
        os.makedirs(path, exist_ok=True)

def main():
    ensure_report_dirs()
    
    for tool in TOOLS:
        run_tool(tool)
    
    print("\n[+] All tools executed. Reports should be in ./reports/info_gathering/<tool>/")

if __name__ == "__main__":
    main()
