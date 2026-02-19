
from google.adk.agents.llm_agent import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai.types import Content, Part
from typing import Any, Dict, Optional


'''
Agent callbacks
In agent callbacks, you can either return Content to change the behavior or None to allow the default behavior.

Here’s an example of before_agent_callback to log agent calls and skip agent execution:

'''

def before_agent_callback(callback_context: CallbackContext) -> Optional[Content]:

    print(f"▶ before_agent_callback")
    print(f"  Agent: {callback_context.agent_name}")
    print(f"  Invocation ID: {callback_context.invocation_id}")
    print(f"  Current State: {callback_context.state.to_dict()}")

    # Return Content to skip agent execution
    test = False
    if test:
        print(f"  Agent execution skipped")
        return Content(
            parts=[
                Part(
                    text=f"Agent '{callback_context.agent_name}' execution skipped by 'before_agent_callback'."
                )
            ],
            role="model",  # Assign model role to the overriding response
        )

    # Allow default behavior
    return None

def after_agent_callback(callback_context: CallbackContext) -> Optional[Content]:

    print(f"▶ after_agent_callback")
    print(f"  Agent: {callback_context.agent_name}")
    print(f"  Invocation ID: {callback_context.invocation_id}")
    print(f"  Current State: {callback_context.state.to_dict()}")

    # Return Content to modify the agent response
    test = False
    if test:
        print(f"  Agent response modified")
        return Content(
            parts=[
                Part(
                    text=f"This is additional response added by 'after_agent_callback'."
                )
            ],
            role="model",  # Assign model role to the overriding response
        )
    # Allow default behavior
    return None

'''
Model callbacks
Model callbacks are similar to agent callbacks but instead you return LlmResponse to alter the behavior and None to allow the default behavior.

Here is a before_model_callback that logs the model call and then skips it:

'''
def before_model_callback(
    callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:

    print(f"▶ before_model_callback")
    print(f"  Agent: {callback_context.agent_name}")
    print(f"  Invocation ID: {callback_context.invocation_id}")

    # Return LlmResponse to skip model call
    test = False
    if test:
        print(f"  Model call skipped")
        return LlmResponse(
            content=Content(
                parts=[Part(text=f"Model call skipped by 'before_model_callback'.")],
                role="model",  # Assign model role to the overriding response
            )
        )
    # Allow default behavior
    return None


def after_model_callback(
    callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:

    # Modify the model response with a new LlmResponse
    test = False
    if test:
        print(f"  Model response modified to be uppercase")
        modified_response = LlmResponse(
            content=Content(
                parts=[
                    Part(
                        text=f"[Modified by after_model_callback] {llm_response.content.parts[0].text.upper()}"
                    )
                ],
                role="model",
            )
        )
        return modified_response

    # Allow default behavior
    return None

'''
Tool callbacks
In tool callbacks, you can log and modify the tool calls.

For example, here’s before_tool_callback to log and skip the tool execution:
'''
def before_tool_callback(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:

    print(f"▶ before_tool_callback")
    print(f"  Agent: {tool_context.agent_name}")
    print(f"  Invocation ID: {tool_context.invocation_id}")
    print(f"  Tool: {tool.name}")
    print(f"  Args: {args}")

    # Return tool response to skip tool execution
    test = False
    if test:
        if tool.name == "get_weather" and args.get("location").lower() == "london":
            tool_response = "The weather in London is always rainy and gloomy."
            print(
                f"  Tool execution skipped for location London and returning tool response: {tool_response}"
            )
            return tool_response

    # Allow default behavior
    return None


def after_tool_callback(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:

    # Modify the tool response
    test = True
    if test:
        if tool.name == "get_weather":
            tool_response = "The weather is always rainy and gloomy."
            print(f"  Tool response modified for 'get_weather' to: {tool_response}")
            return tool_response

    # Allow default behavior
    return None
