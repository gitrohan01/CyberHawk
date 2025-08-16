# core/scan_runner.py
from __future__ import annotations
import subprocess, shlex, re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

BASE_DIR = Path(__file__).resolve().parents[1]
TOOLS = {
    "dig": BASE_DIR / "info_gathering/dig/run.sh",
    "host": BASE_DIR / "info_gathering/host/run.sh",
    "nslookup": BASE_DIR / "info_gathering/nslookup/run.sh",
    "ping": BASE_DIR / "info_gathering/ping/run.sh",
    "traceroute": BASE_DIR / "info_gathering/traceroute/run.sh",
    "whois": BASE_DIR / "info_gathering/whois/run.sh",
}

DOMAIN_RE = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})+$")
IPV4_RE = re.compile(r"^(25[0-5]|2[0-4]\d|[01]?\d?\d)(\.(25[0-5]|2[0-4]\d|[01]?\d?\d)){3}$")
IPV6_RE = re.compile(r"^[0-9A-Fa-f:]+$")

def sanitize_target(target: str) -> str:
    t = target.strip()
    if DOMAIN_RE.match(t) or IPV4_RE.match(t) or IPV6_RE.match(t):
        return t
    raise ValueError("Invalid target (only domain or IP allowed).")

def ensure_report_dir(tool: str, target: str) -> Path:
    d = BASE_DIR / "reports" / "info_gathering" / tool
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{target}_{tool}.txt"

def run_tool(tool: str, target: str, timeout: int = 90) -> Tuple[int, str, str, Optional[Path]]:
    script = TOOLS[tool]
    if not script.exists():
        return (127, "", f"run.sh not found for {tool}", None)
    outfile = ensure_report_dir(tool, target)
    cmd = f"{shlex.quote(str(script))} {shlex.quote(target)}"
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        stdout, stderr, code = proc.stdout, proc.stderr, proc.returncode
        # Save stdout to the canonical report file to keep consistency
        try:
            outfile.write_text(stdout or "", encoding="utf-8", errors="ignore")
        except Exception as e:
            stderr = (stderr or "") + f"\n[write_error:{e}]"
        return (code, stdout, stderr, outfile)
    except subprocess.TimeoutExpired:
        return (124, "", "timeout", None)

def run_info_gathering(target: str) -> Dict[str, Dict]:
    safe_target = sanitize_target(target)
    started = datetime.utcnow()
    results = {}
    for tool in TOOLS:
        code, out, err, path = run_tool(tool, safe_target)
        results[tool] = {
            "returncode": code,
            "stdout": out,
            "stderr": err,
            "report_path": str(path) if path else None,
        }
    results["_meta"] = {"target": safe_target, "started": started.isoformat()}
    return results
