import argparse
import asyncio
import json
import os
import sys
from typing import List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from agent.researcher import AppResearcher
from agent.app_registry import APPS, AppEntry

SAMPLE_10_IDS = [
    "salesforce",      # CRM & Sales
    "zendesk",         # Support & CS
    "slack",           # Comms & Messaging
    "mailchimp",       # Marketing & Social
    "shopify",         # Ecommerce
    "apify",           # Research & Enrichment
    "github",          # Dev, Infra & Data
    "linear",          # Productivity & PM
    "stripe",          # Finance & Fintech
    "fathom"           # AI, Video & Audio
]

async def main():
    parser = argparse.ArgumentParser(description="Run Composio AI Research Agent")
    parser.add_argument("--sample", type=int, default=10, help="Number of sample apps to research (default: 10, 1 per category)")
    parser.add_argument("--all", action="store_true", help="Research all 100 apps")
    parser.add_argument("--app", type=str, help="Research a single specific app ID")
    args = parser.parse_args()

    researcher = AppResearcher(output_dir="data/raw")
    
    if args.app:
        target_apps = [a for a in APPS if a.id == args.app]
        if not target_apps:
            print(f"Error: App ID '{args.app}' not found in registry.")
            return
    elif args.all:
        target_apps = APPS
    else:
        # Default: Pilot run on 10 apps across 10 categories
        target_apps = [a for a in APPS if a.id in SAMPLE_10_IDS]
        if len(target_apps) < args.sample:
            # fill up to requested sample size
            existing_ids = {a.id for a in target_apps}
            for a in APPS:
                if a.id not in existing_ids:
                    target_apps.append(a)
                    if len(target_apps) >= args.sample:
                        break

    print("=" * 65)
    print("🚀 COMPOSIO AI PRODUCT OPS RESEARCH AGENT — LIVE RUN")
    print(f"Target: {len(target_apps)} apps across {len(set(a.category for a in target_apps))} categories")
    print("Engine: Serper API (Search) + Google Gemini-3.6-Flash (Reasoning)")
    print("Integrity: Zero-mock enforcement, caching enabled, rate-limit protected")
    print("=" * 65)

    results = await researcher.research_all(target_apps, delay_seconds=3.0)

    print("\n" + "=" * 65)
    print("📊 COMPILING RESEARCH RESULTS...")
    os.makedirs("data", exist_ok=True)
    
    # Save the current batch
    merged_data = [profile.model_dump(mode='json') for profile in results]
    with open("data/apps_research.json", "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=2)

    print(f"✅ Successfully wrote {len(merged_data)} app profiles to data/apps_research.json")
    print("=" * 65)

if __name__ == "__main__":
    asyncio.run(main())
