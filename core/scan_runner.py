# core/scan_runner.py
import subprocess
import importlib
import sys
import os
import django
from django.utils import timezone

# Setup Django for standalone execution
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cyberhawk.settings")
django.setup()

from core.models import Website, ScanSession, ReconResult


def run_tool(tool_name: str, target: str) -> str:
    """
    Runs a recon tool (via dockerized tool or script) and returns stdout as string.
    """
    print(f"[+] Running {tool_name} on {target} ...")
    try:
        # Adjust this command per your docker setup
        result = subprocess.run(
            ["docker", "run", "--rm", tool_name, target],
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.stdout + ("\n[stderr]\n" + result.stderr if result.stderr else "")
    except Exception as e:
        print(f"[!] Error running {tool_name}: {e}")
        return ""


def parse_and_store(tool_name: str, raw_output: str, website: Website, session: ScanSession):
    """
    Dynamically load <toolname>_parser.py and call `parse(raw_output, website, session)`.
    """
    try:
        parser_module = importlib.import_module(f"parsers.{tool_name}_parser")
        if hasattr(parser_module, "parse"):
            tabular_data = parser_module.parse(raw_output, website, session)
        else:
            tabular_data = {}

        # Always save ReconResult (even if parser fails)
        ReconResult.objects.create(
            session=session,
            website=website,
            target=website.url,
            tool_name=tool_name,
            raw_log=raw_output[:5000],  # truncate if huge
            tabular_data=tabular_data or {}
        )

        print(f"[+] Stored {tool_name} results for {website.url}")

    except ModuleNotFoundError:
        print(f"[!] Parser not found for {tool_name}, storing raw only.")
        ReconResult.objects.create(
            session=session,
            website=website,
            target=website.url,
            tool_name=tool_name,
            raw_log=raw_output[:5000],
            tabular_data={}
        )
    except Exception as e:
        print(f"[!] Parser error for {tool_name}: {e}")


def run_info_gathering(session: ScanSession, target: str, tools: list):
    """
    Run all tools against a target, parse and store results in DB.
    """
    website, _ = Website.objects.get_or_create(url=target)

    session.status = "running"
    session.start_time = timezone.now()
    session.save()

    for tool in tools:
        raw_output = run_tool(tool, target)
        if raw_output:
            parse_and_store(tool, raw_output, website, session)

    session.status = "completed"
    session.end_time = timezone.now()
    session.save()

    print(f"[+] Recon completed for {target}")


if __name__ == "__main__":
    # Example usage
    target_url = "example.com"
    tools_to_run = ["dig", "cmseek"]  # must have parsers/dig_parser.py etc.
    session = ScanSession.objects.create(
        admin_id=1,  # replace with actual admin user id
        name=f"Scan for {target_url}",
        target_input=target_url,
        status="pending"
    )
    run_info_gathering(session, target_url, tools_to_run)


""" need to develope this as final runner """
