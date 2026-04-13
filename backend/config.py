import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ===============================
# AI / LLM Configuration
# ===============================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# ===============================
# Base Paths (OS-safe)
# ===============================
BASE_DIR = os.path.join("backend", "storage")
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "latest")
SCREENSHOT_DIR = os.path.join(OUTPUT_DIR, "screenshots")

# ===============================
# Browser / Execution Config
# ===============================
BROWSER = os.getenv("BROWSER", "chromium")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10000"))
