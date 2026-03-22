"""
Base Agent class — the reusable blueprint all agents inherit from.

This is the pattern the Claude Agent SDK uses under the hood:
- Each agent has a name, a system prompt, and optional tools
- The run() method handles the agent loop (LLM → tool call → result → repeat)
- Subclasses override system_prompt and tools to specialise the agent
"""

import json
import os

from groq import Groq

CHAT_MODEL = "qwen/qwen3-32b"
MAX_ITERATIONS = 10

_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))


class Agent:
    """
    Base class for all agents.

    To create a new agent, subclass this and set:
    - name: a label for logging
    - system_prompt: the agent's role and instructions
    - tools: list of tool definitions (optional)
    """

    name: str = "Agent"
    system_prompt: str = "You are a helpful assistant."
    tools: list = []

    def run(self, user_message: str) -> str:
        """
        Run the agent loop on a user message.
        Returns the agent's final text response.

        Loop:
        1. Send messages to LLM
        2. If LLM wants to call a tool → execute it, feed result back
        3. If LLM gives a text response → return it
        4. Repeat until done or MAX_ITERATIONS reached
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message},
        ]

        for iteration in range(MAX_ITERATIONS):
            # Build the API call — only include tools if this agent has them
            kwargs = {"model": CHAT_MODEL, "messages": messages}
            if self.tools:
                kwargs["tools"] = self.tools
                kwargs["tool_choice"] = "auto"

            response = _groq.chat.completions.create(**kwargs)
            msg = response.choices[0].message

            # If the LLM wants to call tools, execute them and loop again
            if msg.tool_calls:
                messages.append(self._msg_to_dict(msg))
                for tool_call in msg.tool_calls:
                    result = self._execute_tool(tool_call)
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result),
                        }
                    )

            # If the LLM gives a text response, we're done
            else:
                content = msg.content or ""
                # Strip <think>...</think> blocks that qwen3 adds before answering
                import re

                content = re.sub(
                    r"<think>.*?</think>", "", content, flags=re.DOTALL
                ).strip()
                return content

        return "Max iterations reached without a final answer."

    def _execute_tool(self, tool_call) -> str:
        """
        Execute a tool call and return the result as a string.
        Subclasses register their tools in self.available_functions.
        """
        fn_name = tool_call.function.name
        fn_args = json.loads(tool_call.function.arguments)

        if not hasattr(self, "available_functions"):
            return f"Error: no functions registered on {self.name}"

        fn = self.available_functions.get(fn_name)
        if not fn:
            return f"Error: unknown function {fn_name}"

        return fn(**fn_args)

    def _msg_to_dict(self, msg) -> dict:
        """Convert a Groq message object to a plain dict for the messages list."""
        d = {"role": "assistant", "content": msg.content or ""}
        if msg.tool_calls:
            d["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in msg.tool_calls
            ]
        return d
