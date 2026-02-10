import requests
import gc
import torch
from config import OLLAMA_BASE_URL, LLM_MODELS

class LLMManager:
    def __init__(self):
        self.current_model = None

    def unload_model(self):
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
        self.current_model = None

    def load_model(self, mode: str):
        model = LLM_MODELS.get(mode)
        if not model:
            raise ValueError("Invalid LLM mode")

        if self.current_model != model:
            self.unload_model()
            self.current_model = model

        return model

    def generate(self, prompt: str, mode: str):
        model = self.load_model(mode)

        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_ctx": 4096,
                    "temperature": 0.4,
                }
            }
        )

        return response.json()["response"]
