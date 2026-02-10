from models_code.llm_manager import LLMManager
from core.planner import build_prompt

llm = LLMManager()

def explain(context, mode, level):
    prompt = build_prompt(mode, context, level)
    return llm.generate(prompt, mode)
