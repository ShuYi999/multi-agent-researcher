"""
Coordinator — orchestrates the Search Agent and Summariser Agent.

This is the "manager" that:
1. Sends the question to the Search Agent
2. Takes the raw research and passes it to the Summariser Agent
3. Returns the final report

The coordinator itself doesn't search or summarise — it delegates.
"""

from src.search_agent import SearchAgent
from src.summariser_agent import SummariserAgent


class Coordinator:
    def __init__(self):
        self.search_agent = SearchAgent()
        self.summariser_agent = SummariserAgent()

    def run(self, question: str) -> dict:
        print(f"\n[Coordinator] Question: {question}")

        # Step 1: hand off to Search Agent
        print(f"[Coordinator] Handing off to {self.search_agent.name}...")
        raw_research = self.search_agent.run(question)
        print(
            f"[Coordinator] Search complete. Passing to {self.summariser_agent.name}..."
        )

        # Step 2: hand off raw research to Summariser Agent
        summariser_input = f"""Here is the research question: {question}

Here is the raw research gathered:
{raw_research}

Please write a structured report based on this research."""

        report = self.summariser_agent.run(summariser_input)
        print("[Coordinator] Report complete.")

        return {
            "question": question,
            "raw_research": raw_research,
            "report": report,
        }
