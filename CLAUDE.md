# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains two example agents built with Google Agent Development Kit (ADK):

1. **afterschool**: A Python programming tutor agent that helps students learn about dictionaries through an interactive quiz system with comprehensive callback instrumentation
2. **servermanager**: A system monitoring agent that uses parallel and sequential agents to gather CPU, memory, and disk information

Both agents use the ADK framework with LiteLLM for model abstraction (configured via OpenRouter) and Langfuse for observability/tracing.

## Running Agents

Agents are run using the ADK CLI. First, activate the virtual environment:

```bash
source .venv/bin/activate
```

Then run an agent interactively:

```bash
# Run the afterschool tutor agent
python -m google.adk.cli run afterschool.agent:root_agent

# Run the servermanager system monitor
python -m google.adk.cli run servermanager.agent:root_agent
```

To start a web UI for interactive testing:

```bash
python -m google.adk.cli web
```

To start an API server:

```bash
python -m google.adk.cli api_server
```

## Environment Setup

Required environment variables (set in `.env` file):

```
OPENROUTER_API_KEY=<your_key>
LANGFUSE_SECRET_KEY=<your_key>
LANGFUSE_PUBLIC_KEY=<your_key>
LANGFUSE_BASE_URL=<your_url>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Architecture

### Core Framework Concepts

**Agent Types:**
- `LlmAgent`: Single agent that uses an LLM with optional tools
- `ParallelAgent`: Runs multiple sub-agents in parallel, collects outputs
- `SequentialAgent`: Runs sub-agents in sequence, passing state between them

**State Management:**
- Agents share state through `ToolContext.state` or `CallbackContext.state`
- State is dictionary-based and persists across the conversation
- Use `output_key` parameter on agents to store their output in state

**Callbacks (ADK Lifecycle Hooks):**
All callbacks can either return `None` to continue default behavior or return a specific object to override/skip the next step.

- Agent callbacks: `before_agent_callback`, `after_agent_callback`
  - Return `Content` to override behavior
- Model callbacks: `before_model_callback`, `after_model_callback`
  - Return `LlmResponse` to override behavior
- Tool callbacks: `before_tool_callback`, `after_tool_callback`
  - Return dict/object to override tool output

**Tools:**
- Python functions decorated as tools using type hints and docstrings
- Receive `ToolContext` parameter to access state
- Must return dictionary for structured responses

### Project Structure

```
agents/
├── globals.py              # Shared model configuration (LiteLLM + OpenRouter)
├── afterschool/            # Python tutor agent
│   ├── agent.py           # Root agent with callbacks
│   ├── core/
│   │   ├── prompts.py     # Agent instructions with state interpolation
│   │   └── utils.py       # State initialization helpers
│   ├── middleware/
│   │   └── callback.py    # Full callback instrumentation (all 6 callbacks)
│   └── tools/
│       └── tools.py       # Quiz management tools (start, submit, status, reset)
└── servermanager/         # System monitor agent
    ├── agent.py           # SequentialAgent with ParallelAgent sub-agent
    ├── globals.py         # Separate model config for this agent
    └── subagents/         # Modular agent architecture
        ├── cpu/           # CPU info sub-agent
        ├── memory/        # Memory info sub-agent
        ├── disk/          # Disk info sub-agent
        └── analyser/      # Synthesizer that combines all system info

```

### Key Architectural Patterns

**Multi-Agent Orchestration (servermanager):**
- `ParallelAgent` gathers CPU, memory, disk info simultaneously
- Each sub-agent has `output_key` to store results in state
- `SequentialAgent` runs gatherer → analyser pipeline
- Analyser reads from state to synthesize final report

**Callback Instrumentation (afterschool):**
- `before_agent_callback`: Initialize quiz state on first run
- `before_model_callback`: Log/modify LLM requests
- `after_model_callback`: Log/modify LLM responses
- `before_tool_callback`: Log/intercept tool calls
- `after_tool_callback`: Log/modify tool responses
- `after_agent_callback`: Post-processing of agent output

**State Interpolation in Prompts:**
- Prompts use `{variable}` syntax to inject state values
- ADK automatically interpolates these from current state
- Example: `"Current score: {score_percentage}%"` in `prompts.py`

**Tool Design:**
- Tools check state prerequisites (e.g., quiz must be started)
- Tools update state for cross-turn persistence
- Clear error messages returned as dict responses
- Comprehensive docstrings for LLM understanding

## Dependencies

Key packages:
- `google-adk`: Agent Development Kit framework
- `litellm`: Multi-provider LLM abstraction
- `langfuse`: LLM observability and tracing
- `openinference-instrumentation-google-adk`: ADK instrumentation for Langfuse
- `psutil`: System monitoring (for servermanager)
- `rich`: Enhanced console output

## Important Notes

- Both agents are configured to use `openrouter/google/gemini-3-flash-preview` via LiteLLM
- Langfuse instrumentation is enabled at module import time
- The `afterschool` agent demonstrates full callback lifecycle logging
- The `servermanager` agent demonstrates multi-agent orchestration patterns
- Agent modules must expose `root_agent` variable for ADK CLI discovery
