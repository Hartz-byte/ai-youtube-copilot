import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.getenv("AIYC_ROOT")

OLLAMA_BASE_URL = "http://localhost:11434"

CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR")

# VRAM-safe model mapping
LLM_MODELS = {
    "shorts": "llama3:8b-instruct-q4_K_M",
    "long": "llama3:8b-instruct-q4_K_M",
    "code": "mistral:7b-instruct-q4_K_M",
}

EMBED_MODEL = "nomic-embed-text"
