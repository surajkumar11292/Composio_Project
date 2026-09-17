import pytest
from pydantic import ValidationError
from datetime import datetime, timezone
import re

from agent.app_registry import APPS
from agent.models.app_profile import AppProfile, AuthMethod, AccessTier, BuildabilityVerdict

def test_app_registry_count():
    assert len(APPS) == 100, f"Expected 100 apps, found {len(APPS)}"

def test_app_registry_categories():
    categories = {}
    for app in APPS:
        categories[app.category] = categories.get(app.category, 0) + 1
    
    assert len(categories) == 10, f"Expected 10 categories, found {len(categories)}"
    for cat, count in categories.items():
        assert count == 10, f"Expected 10 apps in {cat}, found {count}"

def test_app_registry_unique_ids():
    ids = [app.id for app in APPS]
    assert len(ids) == len(set(ids)), "Duplicate app IDs found"

def test_app_registry_urls():
    url_pattern = re.compile(r'^https?://')
    for app in APPS:
        assert url_pattern.match(app.homepage), f"Invalid URL for {app.id}: {app.homepage}"

def test_app_profile_serialization():
    data = {
        "id": "test_app",
        "name": "Test App",
        "category": "Test Category",
        "auth_methods": [AuthMethod.API_KEY],
        "access_tier": AccessTier.SELF_SERVE_FREE,
        "has_public_docs": True,
        "docs_url": "https://docs.testapp.com",
        "api_type": "REST",
        "has_mcp_server": False,
        "mcp_server_url": None,
        "buildability": BuildabilityVerdict.READY,
        "blocker": None,
        "confidence_score": 0.95,
        "evidence_urls": ["https://docs.testapp.com/auth"],
        "raw_notes": "Looks good.",
        "researched_at": datetime.now(timezone.utc).isoformat()
    }
    
    # Should parse without error
    profile = AppProfile.model_validate(data)
    assert profile.id == "test_app"
    assert profile.auth_methods[0] == AuthMethod.API_KEY
    
    # Test dump
    dumped = profile.model_dump(mode='json')
    assert dumped["id"] == "test_app"

def test_app_profile_invalid_data():
    data = {
        "id": "test_app",
        "name": "Test App",
        # Missing required fields
    }
    with pytest.raises(ValidationError):
        AppProfile.model_validate(data)
