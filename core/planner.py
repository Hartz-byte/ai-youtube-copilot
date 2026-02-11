SYSTEM_CONTEXT = """
You are an expert AI/ML Engineer and Technical Content Creator.
Explain code like a senior engineer during a technical walkthrough.
Be precise, structured, and technical.
"""

def build_code_prompt(file_path, content, structure, level, context):

    level_instruction = {
        "Beginner": "Explain in simple terms.",
        "Student": "Explain technically but clearly.",
        "Interviewer": "Explain deeply with architectural insight and trade-offs."
    }.get(level, "Explain technically.")

    return f"""
{SYSTEM_CONTEXT}

External Context:
{context}

File: {file_path}

Detected Structure:
Functions: {structure.get("functions", [])}
Classes: {structure.get("classes", [])}

Code:
{content}

Instruction:
{level_instruction}

Explain:
1. Overall purpose of the file
2. What each function does
3. Why each function exists
4. Design decisions
5. How this file interacts with other modules
"""

def build_prompt(mode, context, level):
    level_instruction = {
        "Beginner": "Explain in very simple terms with an analogy.",
        "Student": "Explain clearly with technical accuracy.",
        "Interviewer": "Explain deeply with architecture, trade-offs, and real-world usage."
    }[level]

    if mode == "shorts":
        return f"""
{SYSTEM_CONTEXT}

You are generating a YouTube SHORT script.

Topic:
{context}

Instruction:
- Keep it concise (30-60 seconds speaking time).
- Make it engaging.
- Start with a hook.
- Then explain technically.
- End with a strong takeaway.

Level:
{level_instruction}
"""
    else:
        return f"""
{SYSTEM_CONTEXT}

Topic:
{context}

Instruction:
{level_instruction}
"""

def build_diagram_prompt(context: str) -> str:
    return f"""
Generate ONLY valid Mermaid.js diagram code.

Rules:
- Output must start with: graph TD
- DO NOT include markdown fences
- DO NOT include explanations
- Only ONE graph declaration
- No extra text before or after

Context:
{context}
"""
