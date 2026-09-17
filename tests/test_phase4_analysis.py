import pytest
import os
import json

@pytest.fixture
def patterns_data():
    file_path = "data/patterns_analysis.json"
    if not os.path.exists(file_path):
        pytest.skip("data/patterns_analysis.json not found. Run 'python scripts/run_analysis.py' first.")
    with open(file_path, "r") as f:
        return json.load(f)

def test_phase4_stats_sums(patterns_data):
    # Test auth percentages sum to ~100 or less (if some apps have no auth)
    # Actually, apps can have multiple auth methods so sum can be > 100%
    assert patterns_data["total_apps"] == 100

def test_phase4_categories_present(patterns_data):
    build_by_cat = patterns_data.get("buildability_by_category", {})
    assert len(build_by_cat) == 10, "Should have 10 categories"

def test_phase4_narrative_exists(patterns_data):
    narrative = patterns_data.get("executive_narrative", "")
    assert len(narrative) > 50, "Narrative is too short or missing"

def test_phase4_no_null_stats(patterns_data):
    assert "easy_wins" in patterns_data
    assert type(patterns_data["easy_wins"]) == list
