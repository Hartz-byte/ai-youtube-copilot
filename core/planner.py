SYSTEM_CONTEXT = """
You are an expert Technical Content Engineer. Your goal is to explain technical concepts and codebases with 100% accuracy.

STRICT GROUNDING RULES:
1. ONLY mention libraries, functions, and logic that are EXPLICITLY present in the provided source code or context.
2. DO NOT assume the presence of frameworks (like Mongoose, React, MongoDB, etc.) unless you see them in the code.
3. For Python projects: NEVER mention Node.js libraries or MongoDB unless you see 'import pymongo' or equivalent.
4. For acronyms like RAG, always use "Retrieval-Augmented Generation" unless the code defines it otherwise.

STRICT OUTPUT RULES:
1. NO CONVERSATIONAL FILLER. No "Here is the script" or "I've synthesized the data".
2. Start and end DIRECTLY with the content.
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

GUIDELINES:
1. FOCUS ONLY ON CUSTOM LOGIC: If the level is 'Interviewer', SKIP standard framework boilerplate (e.g., Streamlit UI calls, OS pathing, JSON loading). Focus on the ALGORITHMS and ARCHITECTURE.
2. Start with a single sentence summary of the file's role.
3. List what each CUSTOM function/class DOES.
4. If you see a function calling another function, mention that interaction.
5. DO NOT invent external dependencies.

ANALYSIS DATA:
Functions: {structure.get("functions", [])}
Classes: {structure.get("classes", [])}

FULL RAW CODE:
{content}
"""

def build_long_video_synthesis_prompt(explanations, level):
    return f"""
    {SYSTEM_CONTEXT}
    
    You are a Senior Architect delivering a project walkthrough.
    Synthesize the following file analyses into a COHESIVE, HIGH-LEVEL technical story.
    Level: {level}
    
    STRUCTURE:
    - THE HOOK: The core engineering problem solved.
    - THE SYSTEM: High-level architectural flow.
    - THE INNOVATION: 2-3 specific technical "wins" (algorithms or patterns).
    - THE VERDICT: Trade-offs and scalability.
    
    RULES:
    - NO SCENE MARKERS (e.g., [Intro music], [Cut to animation]).
    - NO Interviewer/Host labels.
    - Write it as a professional technical narrative.
    - Focus on the project-specific logic (e.g., CV algorithms, OCR logic).
    
    FILE ANALYSES:
    {explanations}
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
        
        NARRATIVE RULES (MANDATORY):
        1. WORD COUNT: Maximum 150 words.
        2. Persona: A relatable, expert AI Engineer. Talk like a human, not a textbook.
        3. NO META-TAGS: Do NOT use [Hook], labels, or "Host:". Just the script text.
        4. UNIQUE VALUE: You MUST include one "Pro-Tip" or "Common Industry Gotcha" related to {context}.
        5. TONE: Engaging, high-energy, and simple. Use everyday analogies.

        SCRIPT STRUCTURE:
        - Punchy Hook
        - Simple Human-Level Explanation
        - THE PRO-TIP (A specific technique or solution)
        - Final "So What?"

        -------------------------------------------------
        PERSONAL LEARNING APPENDIX:
        After the script, leave EXACTLY THREE EMPTY LINES, then provide the following block:
        
        > [!TIP]
        > ### 🎓 MASTER CLASS PREP
        > {context}
        > - **Definition**: High-level technical definition.
        > - **Deep Nuance 1**: Specific algorithm or system trade-off.
        > - **Deep Nuance 2**: Mathematical or performance property.
        
        Ensure EVERY LINE of the Master Class Prep starts with the "> " character to keep it in a single box.
        -------------------------------------------------
        """
    else:
        # ... [Long video prompt remains same] ...
        return f"""
        {SYSTEM_CONTEXT}
        Create a detailed, deep-dive YouTube video script.
        Topic/Context: {context}
        Level: {level}
        Guidance: {current_level_instr}
        """

def build_diagram_prompt(context):
    return f"""
    {SYSTEM_CONTEXT}
    
    Create a PROFESSIONAL and NON-LINEAR Mermaid.js 'graph TD' diagram for: {context}
    
    VISUAL HIERARCHY RULES:
    1. NON-LINEAR: The flow MUST branch. (e.g., A --> B and A --> C). 
    2. SHAPES: Use [[Subprocess]], [(Database)], {{Decision}} where appropriate.
    3. STYLING (MANDATORY): You MUST include exactly this styling block at the end of the code:
    
    classDef default fill:#1a1c23,stroke:#ff4b4b,stroke-width:2px,color:#fff,rx:10,ry:10
    classDef highlight fill:#ff4b4b,stroke:#fff,stroke-width:3px,color:#fff,font-weight:bold
    classDef data fill:#262730,stroke:#00d2ff,stroke-width:2px,color:#fff
    
    4. Apply classes to at least 2 nodes (e.g., class NodeA highlight).
    
    Return ONLY the raw Mermaid code.
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
