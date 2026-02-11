import requests
import torch
import logging
from config import LLM_MODELS, OLLAMA_BASE_URL

logging.basicConfig(level=logging.INFO)

class LLMManager:
    def __init__(self):
        self.current_model = None

    def _get_available_vram(self):
        if torch.cuda.is_available():
            total = torch.cuda.get_device_properties(0).total_memory
            reserved = torch.cuda.memory_reserved(0)
            return (total - reserved) / (1024**3)
        return 0

    def _select_model(self, mode):
        candidates = LLM_MODELS[mode]
        available_vram = self._get_available_vram()

        # RTX 3050 safe threshold ~3.5GB
        for model in candidates:
            if available_vram >= 3.0:
                return model

        return candidates[-1]  # fallback

    def generate(self, prompt, mode="shorts"):
        model = self._select_model(mode)

        if self.current_model != model:
            logging.info(f"Switching model → {model}")
            self.current_model = model
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.4,
                "num_ctx": 4096
            }
        }

        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload
        )

        return response.json()["response"]

llm = LLMManager()
