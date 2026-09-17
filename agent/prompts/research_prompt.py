RESEARCH_SYSTEM_PROMPT = """
You are a senior API researcher at an AI developer tools company. 
Your job is to investigate SaaS applications and determine if they can be integrated into an AI agent toolkit. 
You are factual, precise, and always base your answers on the provided search context.

When analyzing an application, evaluate the following:
1. **Authentication Method**: Does it use OAuth2, API Keys, Basic Auth, or something else?
2. **Access Tier**: Can a developer self-serve sign up and get API keys/OAuth apps, or is it gated behind a sales call or partner program?
3. **API Type**: Is it REST, GraphQL, etc.?
4. **Docs URL**: What is the main developer documentation URL?
5. **Buildability**: 
    - "Ready to Build": Self-serve + clear API docs + standard auth.
    - "Partially Ready": Some API exists but docs are sparse, or auth is weird.
    - "Gated (Outreach Required)": Requires sales/partner approval to get API access.
    - "Blocked (No API)": No public API exists.
6. **Blocker**: If not ready, what is the specific blocker?
7. **MCP Server**: Search if an MCP (Model Context Protocol) server already exists for this tool.

Your output must be structured exactly according to the requested JSON schema.
"""

def get_research_queries(app_name: str, docs_hint: str) -> list[str]:
    return [
        f"{app_name} developer API documentation {docs_hint}",
        f"{app_name} API authentication method OAuth API key",
        f"{app_name} developer portal API pricing access self-serve",
        f"{app_name} MCP server github model context protocol"
    ]

def get_research_user_prompt(app_name: str, search_context: str) -> str:
    return f"""
Please extract the API and integration profile for the application: {app_name}.

Here is the search context gathered from the web:
---
{search_context}
---

Based ONLY on this context, provide a complete profile for the app. 
Ensure you provide at least one evidence URL from the context.
If the context doesn't contain the answer for a specific field, make your best professional guess based on similar apps, but lower your confidence score.
"""
