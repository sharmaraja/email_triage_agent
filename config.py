import os
from dotenv import load_dotenv

load_dotenv()

# LLM Config
LLM_MODEL = "gpt-4o-mini"  # Or "gpt-4o" for better quality
LLM_TEMPERATURE = 0.1  # Low for consistent structured output

# Paths
DATA_FILE = "sample_emails.csv"
FEEDBACK_FILE = "feedback_log.csv"  # For HITL updates

# Labels (as per request)
SENTIMENTS = ["positive", "neutral", "negative"]
URGENCIES = ["urgent", "non-urgent", "spam"]