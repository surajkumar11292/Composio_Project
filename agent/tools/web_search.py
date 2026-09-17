import os
import json
import hashlib
import aiohttp
from typing import List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
import asyncio

from agent.config import SERPER_API_KEY, TAVILY_API_KEY

CACHE_DIR = os.path.join("data", "cache", "search")
os.makedirs(CACHE_DIR, exist_ok=True)

def _get_cache_path(query: str) -> str:
    query_hash = hashlib.md5(query.strip().lower().encode("utf-8")).hexdigest()
    return os.path.join(CACHE_DIR, f"{query_hash}.json")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=8))
async def serper_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search using Serper API (Google Search engine).
    """
    url = "https://google.serper.dev/search"
    payload = {
        "q": query,
        "num": max_results
    }
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
        async with session.post(url, headers=headers, json=payload) as response:
            response.raise_for_status()
            data = await response.json()
            
            results = []
            for item in data.get("organic", []):
                results.append({
                    "url": item.get("link", ""),
                    "title": item.get("title", ""),
                    "content": item.get("snippet", "")
                })
            return results

async def search_web(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Searches Serper with local disk caching.
    Returns real search results or empty list on failure. Never returns fake mock URLs.
    """
    cache_path = _get_cache_path(query)
    
    # 1. Check local cache
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cached = json.load(f)
                if cached:
                    return cached
        except Exception:
            pass

    # 2. Query Serper
    try:
        results = await serper_search(query, max_results=max_results)
        if results:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
        return results
    except Exception as e:
        print(f"[Warning] Serper search failed for '{query}': {e}")
        return []
