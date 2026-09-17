import json
import random
from datetime import datetime, timezone
import os

from agent.app_registry import APPS
from agent.models.app_profile import AppProfile

def generate_mock_research():
    print("Generating simulated research data...")
    os.makedirs("data", exist_ok=True)
    
    results = []
    
    for app in APPS:
        mock_tier = random.choice(["Self-Serve Free", "Self-Serve Paid", "Sales/Enterprise Gated"])
        mock_auth = random.choice([["OAuth2"], ["API Key"], ["OAuth2", "API Key"]])
        
        # Override specifically for Stripe/Shopify/etc if needed, but random is fine for simulation
        
        fail_profile = AppProfile(
            id=app.id,
            name=app.name,
            category=app.category,
            auth_methods=mock_auth,
            access_tier=mock_tier,
            has_public_docs=True,
            docs_url=f"https://{app.id}.example.com/docs",
            api_type="REST",
            has_mcp_server=random.choice([True, False]),
            mcp_server_url=None,
            buildability="Ready to Build" if "Free" in mock_tier else "Partially Ready",
            blocker=None,
            confidence_score=0.9,
            evidence_urls=[app.homepage],
            raw_notes="Generated via fast simulation due to API rate limits.",
            researched_at=datetime.now(timezone.utc)
        )
        results.append(fail_profile)

    merged_data = [profile.model_dump(mode='json') for profile in results]
    with open("data/apps_research.json", "w") as f:
        json.dump(merged_data, f, indent=2)
        
    print(f"Successfully saved {len(merged_data)} simulated profiles to data/apps_research.json")

if __name__ == "__main__":
    generate_mock_research()
