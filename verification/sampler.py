import json
import random
import os

def sample_apps(seed: int = 42):
    random.seed(seed)
    
    if not os.path.exists("data/apps_research.json"):
        print("Run Phase 3 first.")
        return
        
    with open("data/apps_research.json", "r") as f:
        apps = json.load(f)
        
    categories = {}
    for app in apps:
        cat = app["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(app)
        
    sampled = []
    for cat, items in categories.items():
        chosen = random.choice(items)
        sampled.append({
            "id": chosen["id"],
            "name": chosen["name"],
            "category": chosen["category"],
            "agent_auth_methods": chosen["auth_methods"],
            "agent_access_tier": chosen["access_tier"],
            "evidence_urls": chosen["evidence_urls"]
        })
        
    os.makedirs("verification", exist_ok=True)
    with open("verification/sample_apps.json", "w") as f:
        json.dump(sampled, f, indent=2)
        
    print(f"Sampled {len(sampled)} apps for manual verification.")

if __name__ == "__main__":
    sample_apps()
