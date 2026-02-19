"""
System Monitor Root Agent

This module defines the root agent for the system monitoring application.
It uses a parallel agent for system information gathering and a sequential
pipeline for the overall flow.
"""

from langfuse import get_client
from google.adk.agents import ParallelAgent, SequentialAgent
from openinference.instrumentation.google_adk import GoogleADKInstrumentor

from .subagents.cpu import cpu_info_agent
from .subagents.disk import disk_info_agent
from .subagents.memory import memory_info_agent
from .subagents.analyser import system_report_synthesizer

langfuse = get_client()

# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")

GoogleADKInstrumentor().instrument()

system_info_gatherer = ParallelAgent(
    name="system_info_gatherer",
    sub_agents=[cpu_info_agent, memory_info_agent, disk_info_agent],
)

root_agent = SequentialAgent(
    name="servermanager",
    sub_agents=[system_info_gatherer, system_report_synthesizer],
)