# Multi-Agent Researcher

A multi-agent research system where a Search Agent and a Summariser Agent collaborate to answer questions — each specialised for its own task, coordinated by a central orchestrator.

## What it does

- Search Agent autonomously browses the web to gather raw research
- Summariser Agent reads that research and writes a clean, structured report
- A Coordinator orchestrates the handoff between agents
- Exposes a REST API and a Streamlit chat UI

## Why multiple agents instead of one?

A single agent could theoretically do both jobs, but splitting them produces better results:

| Single agent | Multi-agent |
|---|---|
| Switches between "researcher" and "writer" mindset mid-task | Each agent has one focused job |
| System prompt tries to do too much | Each system prompt is tight and specific |
| Hard to debug which "mode" failed | Clear boundary: search failed vs summarise failed |

This is the **coordinator pattern** — a central orchestrator delegates work to specialist workers and combines their outputs. It's one of the most common multi-agent architectures in production.

## Architecture

```
User question
    ↓
Coordinator
    ↓
Search Agent — agentic loop (search web, read pages, gather raw research)
    ↓
raw research passed as context
    ↓
Summariser Agent — single LLM call (read research, write report)
    ↓
{ raw_research, report } returned to user
```

The UI shows both outputs — the raw research and the final report — so you can see exactly what each agent contributed.

## Tech stack

| Layer | Technology |
|---|---|
| LLM | qwen/qwen3-32b via [Groq](https://groq.com) |
| Web search | DuckDuckGo (via `duckduckgo-search`) |
| Page reading | BeautifulSoup |
| API | FastAPI + Uvicorn |
| UI | Streamlit |

## Project structure

```
multi-agent-researcher/
├── main.py                  # FastAPI app — /research endpoint
├── frontend.py              # Streamlit UI — shows raw research + final report
├── requirements.txt
└── src/
    ├── agent_base.py        # Base Agent class — shared run() loop, tool dispatch
    ├── search_agent.py      # SearchAgent — inherits Agent, adds web search tools
    ├── summariser_agent.py  # SummariserAgent — inherits Agent, no tools
    ├── coordinator.py       # Coordinator — orchestrates agent handoff
    └── tools.py             # search_web and read_page tool definitions
```

## Design decisions

**Why a base `Agent` class with inheritance?**
Both agents share the same core loop: call LLM → check for tool calls → execute tools → repeat. Rather than duplicate this logic, a base `Agent` class implements the shared `run()` loop. Each child class just sets its own `system_prompt` and `tools`. This is the same pattern used by agent SDKs (e.g. Anthropic's Agent SDK).

```python
class Agent:
    system_prompt = "..."
    tools = []

    def run(self, message): ...  # shared loop

class SearchAgent(Agent):
    system_prompt = "You are a web research agent..."
    tools = [search_web, read_page]  # adds tools

class SummariserAgent(Agent):
    system_prompt = "You are a research writer..."
    tools = []  # no tools needed
```

**Why does the Summariser Agent get raw text, not a new question?**
The Coordinator passes the Search Agent's full output as context to the Summariser. This is a deliberate handoff — the Summariser doesn't search again, it only synthesises what was already gathered. Keeping the agents' responsibilities separate makes each one easier to test and replace.

**Why qwen3-32b for both agents?**
The Search Agent needs strong tool-use and reasoning to decide what to search and when to stop. The Summariser needs strong writing ability. A 32B model handles both well. In a cost-sensitive production system you'd route the Summariser to a smaller model since it's a simpler task.

## Getting started

### Prerequisites

- Python 3.11+
- [Groq API key](https://console.groq.com) (free tier available)

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file:

```
GROQ_API_KEY=your_key_here
```

### 3. Start the API

```bash
uvicorn main:app --reload
```

### 4. Start the UI

```bash
streamlit run frontend.py
```

Open `http://localhost:8501` and ask a research question.

## Example questions

- "Any new big AI news?"
- "What is the current state of nuclear fusion energy?"
- "What are the best practices for deploying LLMs in production?"

## Key concepts demonstrated

- **Multi-agent coordination** — coordinator pattern with specialist worker agents
- **Inheritance** — shared base class with specialised child classes
- **Agent handoffs** — structured passing of context between agents
- **Tool use** — LLM-driven web search and page reading
- **Separation of concerns** — each agent has one focused responsibility
