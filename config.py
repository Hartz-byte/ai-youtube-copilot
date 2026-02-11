import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.getenv("AIYC_ROOT")
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR")

OLLAMA_BASE_URL = "http://localhost:11434"

# RTX 3050 Safe Model Mapping
LLM_MODELS = {
    "shorts": ["llama3:8b-instruct-q4_K_M", "mistral:7b-instruct-q4_K_M"],
    "long": ["llama3:8b-instruct-q4_K_M", "mistral:7b-instruct-q4_K_M"],
    "code": ["mistral:7b-instruct-q4_K_M", "llama3:8b-instruct-q4_K_M"],
}

EMBED_MODEL = "nomic-embed-text"

MAX_CONTEXT_CHARS = 12000
MAX_FILES_LONG = 40
MAX_FILES_SHORT = 6
