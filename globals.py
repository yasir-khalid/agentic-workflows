import os
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

model = LiteLlm(
    model="openrouter/google/gemini-3-flash-preview",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
