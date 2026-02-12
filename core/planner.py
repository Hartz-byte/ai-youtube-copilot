SYSTEM_CONTEXT = """
You are an expert Technical Content Engineer. Your goal is to explain technical concepts and codebases with 100% accuracy.

STRICT GROUNDING RULES:
1. ONLY mention libraries, functions, and logic that are EXPLICITLY present in the provided source code or context.
2. DO NOT assume the presence of frameworks (like Mongoose, React, etc.) unless you see them in the code.
3. If the code is Python, do NOT mention Node.js libraries (like Mongoose/Express) unless explicitly imported.
4. For acronyms like RAG, always use "Retrieval-Augmented Generation" unless the code defines it otherwise.
"""

def build_code_prompt(file_path, content, structure, level, context):
    style = "Provide a deep technical walkthrough."
    if level == "Beginner":
        style = "Explain in very simple terms with an analogy."
    elif level == "Student":
        style = "Explain clearly with technical accuracy."
    elif level == "Interviewer":
        style = "Explain deeply with architectural insight, design patterns, and trade-offs."

    return f"""
{SYSTEM_CONTEXT}

Explain the following Python code for an {level} level audience.
Style: {style}

File: {file_path}

EXTERNAL CONTEXT (Use for overview only):
{context}

ANALYSIS DATA (Use ONLY this for function/class details):
Functions: {structure.get("functions", [])}
Classes: {structure.get("classes", [])}

FULL RAW CODE:
{content}

GUIDELINES:
- Start with a single sentence summary of the file's ACTUAL role in the project.
- List what each function/class DOES based ONLY on the provided code.
- Explain technical trade-offs relevant to the {level} level.
- DO NOT invent external dependencies or frameworks not seen in the code.
- If you see a function calling another function, mention the interaction.
"""

def build_prompt(mode, context, level):
    level_instructions = {
        "Beginner": "Use simple intuition and analogies. Avoid all jargon.",
        "Student": "Explain the mechanics and 'how-to'. Use technical terms with brief definitions.",
        "Interviewer": "Focus on system design, trade-offs, and scalability. Why this specific approach?"
    }
    
    current_level_instr = level_instructions.get(level, "")

    if mode == "shorts":
        return f"""
        {SYSTEM_CONTEXT}

        Create a 60-second YouTube Short script about: {context}
        Level: {level} ({current_level_instr})
        
        NARRATIVE RULES:
        - Persona: A professional, helpful AI Engineer talking to the camera.
        - Tone: Conversational, fast-paced, and authoritative.
        - NO META-TAGS: Do not include [Hook], [Definition], or [Key Takeaway] labels in the spoken text.
        - NO "Host:" OR "[Scene]" labels. Just provide the script text to be read.
        - Structure: Start with a punchy hook, move to a clear technical explanation, and end with a "So What?" (why it matters).
        - Flow: Use natural transitions (e.g., "Think of it like...", "But here's the catch...").
        """
    else:
        return f"""
        {SYSTEM_CONTEXT}

        Create a detailed, deep-dive YouTube video script.
        Topic/Context: {context}
        Level: {level}
        Guidance: {current_level_instr}
        
        Structure the response as a cohesive story. Avoid list-style "What/Why" sections. 
        Focus on how the target concept fits into a larger system architecture.
        """

def build_diagram_prompt(context):
    return f"""
    {SYSTEM_CONTEXT}
    
    Create a PROFESSIONAL Mermaid.js 'graph TD' diagram for: {context}
    
    VISUAL RULES:
    1. DO NOT just use a straight line (A->B->C). Create a branching or circular flow.
    2. Use subgraphs to group related components (e.g., "Data Layer", "Processing").
    3. Use varied node shapes: ([Start/End]), [[Sub-process]], {{Decision}}.
    4. Apply custom styles AT THE END of the graph definition:
    
    classDef default fill:#1a1c23,stroke:#ff4b4b,stroke-width:2px,color:#fff,rx:10,ry:10
    classDef highlight fill:#ff4b4b,stroke:#fff,stroke-width:3px,color:#fff,font-weight:bold
    classDef data fill:#262730,stroke:#00d2ff,stroke-width:2px,color:#fff
    
    To apply a class, use: class NodeID highlight
    Return ONLY the Mermaid code. No markdown fences.
    """

def build_verification_prompt(original_output, context):
    return f"""
    You are a Technical Fact-Checker. 
    Compare the following generated output against the provided source code context.
    
    GENERATED OUTPUT:
    {original_output}
    
    SOURCE CONTEXT:
    {context}
    
    RULES:
    1. If the output is 100% grounded, return ONLY the word: "VERIFIED"
    2. If there are hallucinations, return a single list titled "Hallucinations Found:"
    3. NO CONVERSATIONAL FILLER. NO EXPLANATIONS.
    """
