## Agentic workflows with Google Agent Development Kit (ADK)

At its core, an agent framework like ADK gives you a sequence of steps:

`receive input` → `invoke model` → `invoke tools` → `return output`

In real-world systems, we often need to hook into these steps for logging, guarding, caching, altering prompts or results, or dynamically changing behaviour based on session state. That’s exactly where callbacks come in. Think of callbacks as “checkpoints” in the agent’s lifecycle. The ADK framework automatically calls your functions at these key stages, giving you a chance to intervene.

The ADK (Agent Development Kit) provides three main pairs of callbacks:

#### Agent callbacks:
1. before_agent_callback: Runs just before the agent’s main logic starts.
2. after_agent_callback: Runs just after the agent has produced its final result.

#### Model callbacks:
1. before_model_callback: Runs right before the request is sent to the LLM.
2. after_model_callback: Runs right after the response is received from the LLM.

#### Tool callbacks:
1. before_tool_callback: Runs before a tool (like a Python function) is executed.
2. after_tool_callback: Runs after the tool has returned its result.
You can either observe and modify data in place (e.g., logging a request) or override the default behavior entirely (e.g., blocking the request, providing a cached response).

To observe and let execution continue, your callback function should return **None**.
To override and skip the next step, your callback function should return a specific object (like an LlmResponse or types.Content) depending on the type of the callback.

