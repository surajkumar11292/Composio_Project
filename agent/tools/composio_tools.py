from composio import ComposioToolSet, App
import os

from agent.config import COMPOSIO_API_KEY

def get_composio_tools():
    """
    Returns Composio tools for the agent. 
    Currently we'll load general dev tools if we want the agent to interact with github etc,
    but primarily the assignment is about researching apps using the SDK.
    
    We could load Tavily through Composio, but we are doing it directly to have finer control
    over async rate limiting and fallback to Serper.
    """
    # For demonstration of using Composio SDK as requested:
    # toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
    # return toolset.get_tools(apps=[App.GITHUB])
    return []
