"""
Search Agent — finds information on the web.

This agent's only job is to search and read pages.
It inherits the agent loop from Agent and adds its own tools.
"""

from src.agent_base import Agent
from src.tools import AVAILABLE_FUNCTIONS, TOOLS


class SearchAgent(Agent):
    name = "Search Agent"
    system_prompt = """You are a web research agent. Your job is to find accurate,
up-to-date information on a given topic.

Use search_web to find relevant pages, then read_page to get the full content
of the most promising results. Gather enough information to give a thorough answer.

Return all the raw information you find — don't summarise yet, just collect the facts."""
    tools = TOOLS
    available_functions = AVAILABLE_FUNCTIONS
