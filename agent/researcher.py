import json
import os
import sys
import re
import asyncio
from typing import List, Optional
from datetime import datetime, timezone

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import google.generativeai as genai

from agent.config import GEMINI_API_KEY
from agent.app_registry import AppEntry
from agent.models.app_profile import AppProfile, AuthMethod, AccessTier, BuildabilityVerdict
from agent.tools.web_search import search_web
from agent.prompts.research_prompt import RESEARCH_SYSTEM_PROMPT

# Configure Gemini with verified models
genai.configure(api_key=GEMINI_API_KEY)
PRIMARY_MODEL = "gemini-3.5-flash-lite"
FALLBACK_MODEL = "gemini-3.5-flash"

primary_model = genai.GenerativeModel(PRIMARY_MODEL, system_instruction=RESEARCH_SYSTEM_PROMPT)
fallback_model = genai.GenerativeModel(FALLBACK_MODEL, system_instruction=RESEARCH_SYSTEM_PROMPT)

def clean_json_response(text: str) -> str:
    """Strip markdown backticks if present."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()

class AppResearcher:
    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    async def _generate_with_fallback(self, prompt: str) -> str:
        """Calls primary model, falls back to secondary, and retries on 429 if needed."""
        for attempt in range(3):
            # Try primary
            try:
                res = await primary_model.generate_content_async(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json",
                        temperature=0.1
                    )
                )
                return res.text
            except Exception as e_prim:
                err_str = str(e_prim)
                if "429" in err_str:
                    # Try secondary model
                    try:
                        res = await fallback_model.generate_content_async(
                            prompt,
                            generation_config=genai.GenerationConfig(
                                response_mime_type="application/json",
                                temperature=0.1
                            )
                        )
                        return res.text
                    except Exception as e_sec:
                        print(f"  [Rate limit wait] Both models hit 429. Sleeping 12s (attempt {attempt+1}/3)...")
                        await asyncio.sleep(12)
                        continue
                else:
                    raise e_prim
        raise RuntimeError("Exceeded maximum retries for Gemini API calls")

    async def research_app(self, app: AppEntry, delay_seconds: float = 3.0) -> AppProfile:
        output_file = os.path.join(self.output_dir, f"{app.id}.json")
        
        # Check if already researched successfully from a real run
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    notes = data.get("raw_notes", "")
                    blocker = str(data.get("blocker", ""))
                    # Only reuse if it is genuine, clean, and not an error fallback
                    if (
                        "simulation" not in notes 
                        and "fallback mock" not in notes 
                        and "example.com" not in str(data.get("evidence_urls", []))
                        and "429" not in blocker
                        and "extraction error" not in blocker.lower()
                    ):
                        print(f"  ⏩ Using cached profile for {app.name} ({app.category})")
                        return AppProfile.model_validate(data)
            except Exception:
                pass

        print(f"\n🔍 [{app.category}] Researching: {app.name}...")

        # 1. Search for real docs using Serper
        queries = [
            f"{app.name} API developer documentation authentication OAuth API key",
            f"{app.name} API developer access pricing self-serve gated MCP"
        ]

        evidence_urls = []
        context_blocks = []

        for q in queries:
            results = await search_web(q, max_results=3)
            for res in results:
                url = res.get("url", "").strip()
                title = res.get("title", "").strip()
                snippet = res.get("content", "").strip()
                if url:
                    if url not in evidence_urls:
                        evidence_urls.append(url)
                    context_blocks.append(f"Source URL: {url}\nTitle: {title}\nSnippet: {snippet}\n")

        search_context = "\n---\n".join(context_blocks)
        if not search_context:
            search_context = f"No search results returned for {app.name}. Homepage: {app.homepage}"

        # 2. Prompt Gemini for structured analysis
        prompt = f"""Analyze the application '{app.name}' ({app.category}) for inclusion in an AI agent toolkit.
Official Homepage: {app.homepage}

Web Search Findings:
{search_context}

Output a strictly valid JSON object with EXACTLY these keys:
{{
  "auth_methods": ["OAuth2" | "API Key" | "Basic Auth" | "JWT" | "OAuth1" | "Unknown"],
  "access_tier": "Self-Serve Free" | "Self-Serve Paid" | "Partner/Approval Gated" | "Sales/Enterprise Gated" | "No Public API",
  "has_public_docs": true | false,
  "docs_url": "<main developer documentation URL found in evidence or official portal>",
  "api_type": "REST" | "GraphQL" | "Webhooks" | "gRPC" | "None",
  "has_mcp_server": true | false,
  "mcp_server_url": null,
  "buildability": "Ready to Build" | "Partially Ready" | "Gated (Outreach Required)" | "Blocked (No API)",
  "blocker": null or "<specific blocker if not Ready to Build>",
  "confidence_score": <float between 0.2 and 1.0>,
  "raw_notes": "<concise 2-3 sentence executive summary of findings and credentials access>"
}}
Return ONLY the raw JSON object, without explanation."""

        try:
            # Respect rate limits
            await asyncio.sleep(delay_seconds)

            raw_text = await self._generate_with_fallback(prompt)
            clean_text = clean_json_response(raw_text)
            parsed = json.loads(clean_text)

            # Ensure essential keys and evidence
            parsed["id"] = app.id
            parsed["name"] = app.name
            parsed["category"] = app.category
            parsed["evidence_urls"] = evidence_urls[:5]
            parsed["researched_at"] = datetime.now(timezone.utc).isoformat()

            # Ensure valid docs_url fallback from evidence if missing
            if not parsed.get("docs_url") and evidence_urls:
                parsed["docs_url"] = evidence_urls[0]

            profile = AppProfile.model_validate(parsed)

            # Save real verified result
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(profile.model_dump_json(indent=2))

            print(f"  ✅ {app.name}: Auth={','.join([a.value for a in profile.auth_methods])} | Tier={profile.access_tier.value} | Verdict={profile.buildability.value}")
            return profile

        except Exception as e:
            print(f"  ⚠️ Extraction error for {app.name}: {e}")
            fallback_profile = AppProfile(
                id=app.id,
                name=app.name,
                category=app.category,
                auth_methods=[AuthMethod.UNKNOWN],
                access_tier=AccessTier.PARTNER_GATED,
                has_public_docs=bool(evidence_urls),
                docs_url=evidence_urls[0] if evidence_urls else app.homepage,
                api_type="REST",
                has_mcp_server=False,
                mcp_server_url=None,
                buildability=BuildabilityVerdict.PARTIAL,
                blocker=f"API extraction error: {str(e)[:100]}",
                confidence_score=0.3,
                evidence_urls=evidence_urls[:3],
                raw_notes=f"Search retrieved {len(evidence_urls)} sources. LLM call error: {str(e)[:100]}.",
                researched_at=datetime.now(timezone.utc)
            )
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(fallback_profile.model_dump_json(indent=2))
            return fallback_profile

    async def research_all(self, apps: List[AppEntry], delay_seconds: float = 3.0) -> List[AppProfile]:
        results = []
        for i, app in enumerate(apps, 1):
            print(f"[{i}/{len(apps)}] Processing {app.name}...")
            profile = await self.research_app(app, delay_seconds=delay_seconds)
            results.append(profile)
        return results
