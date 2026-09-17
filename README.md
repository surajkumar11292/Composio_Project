# Composio AI Product Ops Intern — Take-Home Assignment

## Overview
This project contains an AI research agent that profiles 100 apps across 10 categories, extracting their auth methods, API access tiers, and buildability. The results are presented in a self-contained HTML case study dashboard.

## Architecture
The agent uses:
- **Composio Python SDK** for orchestration and tool connections
- **Gemini 2.0 Flash** for reasoning and structured data extraction
- **Tavily** & **Serper** for deep web research

## Setup
1. Clone this repository
2. Run `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your API keys

## Running the Agent
`python scripts/run_agent.py`

## Running Verification
`python scripts/run_verification.py`

## Building Dashboard
`python scripts/build_dashboard.py`
