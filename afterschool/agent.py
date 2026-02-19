"""
System Monitor Root Agent

This module defines the root agent for the system monitoring application.
It uses a parallel agent for system information gathering and a sequential
pipeline for the overall flow.
"""

from langfuse import get_client
from rich import print
from google.adk.agents import ParallelAgent, SequentialAgent
from openinference.instrumentation.google_adk import GoogleADKInstrumentor
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from typing import Optional
from afterschool.tools.tools import (
    get_quiz_questions,
    start_quiz,
    submit_answer,
    get_current_question,
    get_quiz_status,
    reset_quiz,
)
from globals import model
from afterschool.core.prompts import BASE_PROMPT, QUIZ_INSTRUCTIONS
from afterschool.core.utils import initialize_quiz_state
from afterschool.middleware.callback import after_agent_callback, before_model_callback, after_model_callback, before_tool_callback, after_tool_callback

langfuse = get_client()

# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")

GoogleADKInstrumentor().instrument()


def before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """Initialize quiz state if not already present"""
    initialize_quiz_state(callback_context.state)
    print(f"▶ before_agent_callback")
    print(f"  Agent: {callback_context.agent_name}")
    print(f"  Invocation ID: {callback_context.invocation_id}")
    print(f"  Current State: {callback_context.state.to_dict()}")
    
    return None

quiz_tools = [
    get_quiz_questions,
    start_quiz,
    submit_answer,
    get_current_question,
    get_quiz_status,
    reset_quiz,
]

root_agent = LlmAgent(
    model=model,
    name="Afterschool",
    instruction=BASE_PROMPT + QUIZ_INSTRUCTIONS,
    tools=quiz_tools,
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback
)