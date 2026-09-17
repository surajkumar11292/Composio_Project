from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class AuthMethod(str, Enum):
    OAUTH2 = "OAuth2"
    API_KEY = "API Key"
    BASIC_AUTH = "Basic Auth"
    JWT = "JWT"
    OAUTH1 = "OAuth1"
    UNKNOWN = "Unknown"

class AccessTier(str, Enum):
    SELF_SERVE_FREE = "Self-Serve Free"
    SELF_SERVE_PAID = "Self-Serve Paid"
    PARTNER_GATED = "Partner/Approval Gated"
    SALES_GATED = "Sales/Enterprise Gated"
    NO_PUBLIC_API = "No Public API"

class BuildabilityVerdict(str, Enum):
    READY = "Ready to Build"
    PARTIAL = "Partially Ready"
    GATED = "Gated (Outreach Required)"
    BLOCKED = "Blocked (No API)"

class AppProfile(BaseModel):
    # Identity
    id: str
    name: str
    category: str
    
    # Research Results
    auth_methods: List[AuthMethod]
    access_tier: AccessTier
    has_public_docs: bool
    docs_url: Optional[str]
    api_type: Optional[str]           # REST, GraphQL, gRPC, WebSocket
    has_mcp_server: bool
    mcp_server_url: Optional[str]
    
    # Verdict
    buildability: BuildabilityVerdict
    blocker: Optional[str]            # Main blocker if not READY
    confidence_score: float           # 0.0-1.0 agent confidence
    
    # Evidence
    evidence_urls: List[str]          # Doc URLs agent used
    raw_notes: str                    # Agent's raw reasoning
    
    # Meta
    researched_at: datetime
    agent_version: str = "1.0.0"
    manually_verified: bool = False
    verification_notes: Optional[str] = None
