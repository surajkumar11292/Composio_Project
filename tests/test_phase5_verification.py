import pytest
import os
import json

@pytest.fixture
def verification_report():
    file_path = "verification/accuracy_report.json"
    if not os.path.exists(file_path):
        pytest.skip("verification/accuracy_report.json not found.")
    with open(file_path, "r") as f:
        return json.load(f)

def test_phase5_sample_count(verification_report):
    assert verification_report["total_sampled"] == 10

def test_phase5_accuracy_metrics(verification_report):
    assert "auth_accuracy" in verification_report
    assert "access_tier_accuracy" in verification_report
    assert "overall_accuracy" in verification_report
    
    assert 0 <= verification_report["auth_accuracy"] <= 100
    assert 0 <= verification_report["overall_accuracy"] <= 100

def test_phase5_progression_metrics(verification_report):
    assert "first_pass_accuracy" in verification_report
    assert "final_accuracy" in verification_report
    assert verification_report["final_accuracy"] >= verification_report["first_pass_accuracy"]

def test_phase5_results_data(verification_report):
    results = verification_report["verification_results"]
    assert len(results) == 10
    for r in results:
        assert "auth_match" in r
        assert "tier_match" in r
        assert "notes" in r
        assert len(r["notes"]) > 0
