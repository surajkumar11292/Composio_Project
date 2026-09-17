import asyncio
import json
import os
from agent.researcher import AppResearcher
from agent.app_registry import APPS

async def main():
    print("Initializing Composio AI Research Agent...")
    researcher = AppResearcher(output_dir="data/raw")
    
    print(f"Loaded {len(APPS)} apps from registry.")
    print("Starting research pipeline. This may take a while depending on concurrency and rate limits...")
    
    # Run the orchestrator
    results = await researcher.research_all(APPS)
    
    print("\nResearch complete! Merging results...")
    
    # Merge into a single JSON
    merged_data = [profile.model_dump(mode='json') for profile in results]
    os.makedirs("data", exist_ok=True)
    with open("data/apps_research.json", "w") as f:
        json.dump(merged_data, f, indent=2)
        
    print(f"Successfully saved {len(merged_data)} profiles to data/apps_research.json")

if __name__ == "__main__":
    asyncio.run(main())
