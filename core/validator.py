from models_code.llm_manager import LLMManager
from core.planner import build_verification_prompt

class Validator:
    def __init__(self):
        self.llm = LLMManager()

    def verify_grounding(self, output: str, context: str) -> str:
        """
        Runs a second LLM pass to verify if the output is grounded in the provided context.
        """
        print("[*] Running Hallucination Check...")
        prompt = build_verification_prompt(output, context)
        
        # We use the 'code' mode (Mistral) for verification as it's better at precise comparison
        verification_result = self.llm.generate(prompt, mode="code")
        
        if "VERIFIED" in verification_result.upper():
            print("[+] Content verified as grounded.")
            return None
        else:
            print("[!] Hallucinations detected or unverified claims found.")
            return verification_result
