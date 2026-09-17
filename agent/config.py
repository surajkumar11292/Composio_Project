import os
from dotenv import load_dotenv

load_dotenv()

COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

REQUIRED_KEYS = [
    ("COMPOSIO_API_KEY", COMPOSIO_API_KEY),
    ("GEMINI_API_KEY", GEMINI_API_KEY),
    ("TAVILY_API_KEY", TAVILY_API_KEY),
    ("SERPER_API_KEY", SERPER_API_KEY)
]

def validate_config():
    missing_keys = [key for key, value in REQUIRED_KEYS if not value]
    if missing_keys:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_keys)}. Please check your .env file.")

validate_config()

MAX_RETRIES = 3
REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 1.0
