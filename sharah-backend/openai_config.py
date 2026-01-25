from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize async OpenAI client (optional - only if API key is provided)
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = AsyncOpenAI(api_key=api_key)
    model = "gpt-4o-mini"
else:
    client = None
    model = None
    print("Warning: OPENAI_API_KEY not set. OpenAI features will be disabled.")