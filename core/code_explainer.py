from models_code.llm_manager import LLMManager
from core.planner import build_code_prompt

llm = LLMManager()

def explain_code(file, concise=False):
    if not file["analysis"]:
        return None

    prompt = build_code_prompt(
        file["path"],
        file["analysis"],
        level="Interviewer",
        concise=concise
    )
    return llm.generate(prompt, mode="code")
