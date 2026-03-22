"""
Summariser Agent — turns raw research into a clean, structured report.

This agent has NO tools — it only reads text and writes a summary.
It receives raw research from the Search Agent and produces the final answer.
"""

from src.agent_base import Agent


class SummariserAgent(Agent):
    name = "Summariser Agent"
    system_prompt = """You are an expert research writer. Your job is to take raw
research notes and turn them into a clear, well-structured report.

Structure your response as:
## Summary
A 2-3 sentence overview of the key answer.

## Key Findings
Bullet points of the most important facts.

## Details
A fuller explanation with context.

Write clearly. Avoid jargon. Cite specific facts from the research provided."""
    tools = []  # no tools needed — this agent only reads and writes
