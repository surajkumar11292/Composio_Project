import os
import json
import pytest
from datetime import datetime
from agent.models.app_profile import AppProfile

# We only run these tests if the apps_research.json exists, 
# otherwise we skip them because Phase 3 hasn't been executed yet.

@pytest.fixture
def merged_data():
    file_path = "data/apps_research.json"
    if not os.path.exists(file_path):
        pytest.skip("data/apps_research.json not found. Run 'python scripts/run_agent.py' first.")
    with open(file_path, "r") as f:
        return json.load(f)

def test_phase3_data_completeness(merged_data):
    assert len(merged_data) == 100, f"Expected 100 profiles, got {len(merged_data)}"

def test_phase3_valid_profiles(merged_data):
    for app_data in merged_data:
        # Pydantic validation
        profile = AppProfile.model_validate(app_data)
        
        # Check non-empty
        assert len(profile.auth_methods) > 0, f"App {profile.id} has no auth methods"
        if profile.confidence_score > 0.0:
            assert len(profile.evidence_urls) > 0, f"App {profile.id} has no evidence URLs"

def test_phase3_unique_ids(merged_data):
    ids = [app["id"] for app in merged_data]
    assert len(ids) == len(set(ids)), "Duplicate IDs found in merged results"
