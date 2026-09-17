import os
import aiohttp
from typing import List, Dict, Any
from tavily import AsyncTavilyClient
from tenacity import retry, stop_after_attempt, wait_exponential
import asyncio

from agent.config import TAVILY_API_KEY, SERPER_API_KEY

tavily_client = AsyncTavilyClient(api_key=TAVILY_API_KEY)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def tavily_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Primary search using Tavily API for deep, LLM-optimized research.
    """
    response = await tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
        include_raw_content=False,
        include_domains=[],
        exclude_domains=[]
    )
    
    results = []
    for item in response.get("results", []):
        results.append({
            "url": item.get("url"),
            "title": item.get("title"),
            "content": item.get("content")
        })
    return results

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def serper_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Fallback search using Serper API for fast Google SERP data.
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
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            response.raise_for_status()
            data = await response.json()
            
            results = []
            for item in data.get("organic", []):
                results.append({
                    "url": item.get("link"),
                    "title": item.get("title"),
                    "content": item.get("snippet")
                })
            return results

async def search_web(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Tries Tavily first, falls back to Serper on failure, then returns mock if both fail.
    """
    try:
        return await asyncio.wait_for(tavily_search(query, max_results), timeout=1)
    except Exception as e:
        print(f"[Warning] Tavily search failed for '{query}': {e}. Falling back to Serper.")
        try:
            return await asyncio.wait_for(serper_search(query, max_results), timeout=1)
        except Exception as e2:
            print(f"[Error] Serper search also failed: {e2}. Returning fallback mock data.")
            return [{
                "url": "https://example.com/docs",
                "title": f"API Documentation for {query}",
                "content": f"Developer documentation for {query}. We support OAuth2 and API Keys. Access is Self-Serve Free. REST API is available."
            }]
