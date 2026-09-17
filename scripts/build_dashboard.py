import json
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.truth_check import run_truth_check

def build_dashboard(research_file="data/apps_research.json", html_file="dashboard/index.html"):
    print("=" * 60)
    print("🏗️ BUILDING DASHBOARD FROM REAL RESEARCH DATA")
    print(f"Source: {research_file}")
    print(f"Target: {html_file}")
    print("=" * 60)

    # 1. Run strict anti-mock verification first
    if not os.path.exists(research_file):
        print(f"Error: '{research_file}' not found. Run 'python scripts/run_agent.py' first.")
        sys.exit(1)
        
    try:
        run_truth_check(research_file)
    except SystemExit as e:
        if e.code != 0:
            print("❌ Build halted: Truth check failed.")
            sys.exit(1)

    # 2. Load genuine researched apps
    with open(research_file, "r", encoding="utf-8") as f:
        apps = json.load(f)

    # Convert to the dashboard representation
    dashboard_apps = []
    for app in apps:
        auth_methods = app.get("auth_methods", ["Unknown"])
        tier = app.get("access_tier", "Unknown")
        verdict_str = app.get("buildability", "Partially Ready")
        
        if "Ready to Build" in verdict_str:
            verdict = "ready"
        elif "Gated" in verdict_str:
            verdict = "gated"
        elif "Blocked" in verdict_str:
            verdict = "blocked"
        else:
            verdict = "partial"

        docs_url = app.get("docs_url")
        if not docs_url and app.get("evidence_urls"):
            docs_url = app["evidence_urls"][0]
        if not docs_url:
            docs_url = "https://developer.composio.dev"

        dashboard_apps.append({
            "n": app.get("name", "Unknown"),
            "cat": app.get("category", "General"),
            "auth": auth_methods,
            "tier": tier,
            "api": app.get("api_type", "REST"),
            "verdict": verdict,
            "blocker": app.get("blocker"),
            "mcp": bool(app.get("has_mcp_server", False)),
            "docs": docs_url
        })

    # Format JSON
    apps_js = "const APPS = " + json.dumps(dashboard_apps, indent=2) + ";"

    # 3. Read existing HTML
    if not os.path.exists(html_file):
        print(f"Error: {html_file} does not exist.")
        sys.exit(1)

    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Replace the const APPS = [...]; section
    pattern = r"const APPS = \[[\s\S]*?\];"
    if not re.search(pattern, html_content):
        print("Error: Could not locate 'const APPS = [...];' in index.html")
        sys.exit(1)

    updated_html = re.sub(pattern, apps_js, html_content)

    # Write back
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(updated_html)

    print(f"✅ Successfully injected {len(dashboard_apps)} real researched apps into {html_file}")
    print("=" * 60)

if __name__ == "__main__":
    build_dashboard()
