import json
import os
import sys
import asyncio
from typing import Dict, Any
from collections import Counter
import google.generativeai as genai

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from agent.config import GEMINI_API_KEY
from agent.prompts.synthesis_prompt import SYNTHESIS_SYSTEM_PROMPT, get_synthesis_user_prompt

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3.5-flash-lite', system_instruction=SYNTHESIS_SYSTEM_PROMPT)

def compute_stats(apps: list) -> Dict[str, Any]:
    total_apps = len(apps)
    if total_apps == 0:
        return {}
    
    auth_counts = Counter()
    for app in apps:
        for auth in app.get("auth_methods", []):
            auth_counts[auth] += 1
            
    tier_counts = Counter([app.get("access_tier") for app in apps])
    build_counts = Counter([app.get("buildability") for app in apps])
    
    # Buildability by category
    category_build = {}
    for app in apps:
        cat = app.get("category", "General")
        if cat not in category_build:
            category_build[cat] = {"READY": 0, "PARTIAL": 0, "GATED": 0, "BLOCKED": 0}
        
        status = app.get("buildability")
        if status == "Ready to Build":
            category_build[cat]["READY"] += 1
        elif status == "Partially Ready":
            category_build[cat]["PARTIAL"] += 1
        elif status == "Gated (Outreach Required)":
            category_build[cat]["GATED"] += 1
        else:
            category_build[cat]["BLOCKED"] += 1
            
    mcp_coverage = {
        "has_mcp": sum(1 for app in apps if app.get("has_mcp_server")),
        "no_mcp": sum(1 for app in apps if not app.get("has_mcp_server"))
    }
    
    easy_wins = [app.get("name") for app in apps if app.get("buildability") == "Ready to Build" and "Free" in str(app.get("access_tier", ""))]
    
    blockers = Counter([app.get("blocker") for app in apps if app.get("blocker")])
    top_blockers = [b[0] for b in blockers.most_common(5)]
    
    return {
        "total_apps": total_apps,
        "auth_distribution": {k: {"count": v, "pct": round(v/total_apps*100, 1)} for k, v in auth_counts.items()},
        "access_tier_distribution": {k: {"count": v, "pct": round(v/total_apps*100, 1)} for k, v in tier_counts.items()},
        "buildability_distribution": {k: {"count": v, "pct": round(v/total_apps*100, 1)} for k, v in build_counts.items()},
        "buildability_by_category": category_build,
        "mcp_coverage": mcp_coverage,
        "easy_wins": easy_wins,
        "top_blockers": top_blockers
    }

async def generate_narrative(stats: Dict[str, Any]) -> str:
    prompt = f"""Based on the following real research data across {stats.get('total_apps', 0)} SaaS applications, generate a concise, senior-level AI Product Ops executive summary.

Data:
{json.dumps(stats, indent=2)}

Format with:
- Key Takeaway (1-2 sentences)
- Dominant Auth & Gating Patterns
- Fast-Track Immediate Opportunities
- Recommended Composio Strategy (MCP Gateway)
Keep it factual, sharp, and data-backed."""

    try:
        res = await model.generate_content_async(prompt)
        return res.text.strip()
    except Exception as e:
        print(f"[Warning] LLM narrative generation failed: {e}. Using deterministic synthesis.")
        ready_pct = stats.get('buildability_distribution', {}).get('Ready to Build', {}).get('pct', 0)
        oauth_pct = stats.get('auth_distribution', {}).get('OAuth2', {}).get('pct', 0)
        return f"""### AI Product Ops Executive Synthesis
- **Readiness**: {ready_pct}% of analyzed platforms are immediately Ready to Build with public REST/GraphQL APIs and self-serve access.
- **Authentication**: OAuth2 dominates ({oauth_pct}%), requiring token lifecycle and refresh handling.
- **Strategic Path**: Leveraging Composio MCP Gateway addresses the authentication fragmentation across platforms and accelerates time-to-market.
"""

async def main():
    print("Loading apps research data...")
    if not os.path.exists("data/apps_research.json"):
        print("Error: data/apps_research.json not found.")
        return
        
    with open("data/apps_research.json", "r", encoding="utf-8") as f:
        apps = json.load(f)
        
    print(f"Computing statistics for {len(apps)} apps...")
    stats = compute_stats(apps)
    
    print("Generating executive narrative with Gemini-3.6-Flash...")
    narrative = await generate_narrative(stats)
    stats["executive_narrative"] = narrative
    
    os.makedirs("data", exist_ok=True)
    with open("data/patterns_analysis.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
        
    print("✅ Patterns Analysis Complete saved to data/patterns_analysis.json")

if __name__ == "__main__":
    asyncio.run(main())
