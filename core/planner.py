SYSTEM_CONTEXT = """
You are an expert AI/ML Engineer and Technical Content Creator.
Your goal is to explain complex technical concepts, tools, and code repositories.
Always assume the context is related to Artificial Intelligence, Machine Learning, or Software Engineering.

CRITICAL TECHNICAL GROUNDING:
- RAG = Retrieval-Augmented Generation (Retrieving external data to ground LLM responses). It is NOT "Reusable AI Components".
- LLM = Large Language Model
- NLP = Natural Language Processing
- RAG works by: 1. Chunking data, 2. Embedding chunks, 3. Storing in Vector DB, 4. Retrieving relevant chunks during query.

Never provide non-technical or made-up definitions. If you are unsure, focus on the engineering trade-offs of the technical concept.
"""

def build_code_prompt(file_path, analysis, level, concise=False):
    style = "Keep it very short and high-level." if concise else "Provide a deep technical walkthrough."
    
    return f"""
{SYSTEM_CONTEXT}

Explain the following Python code like an interviewer would expect.
Style: {style}

File: {file_path}
Level: {level}

Functions:
{analysis['functions']}

Classes:
{analysis['classes']}

Explain:
- What each function does
- Why it exists
- How it interacts with others
"""

def build_prompt(mode, context, level):
    level_instructions = {
        "Beginner": "Use analogies, avoid jargon, focus on the 'What'.",
        "Student": "Explain how it works step-by-step, use technical terms correctly.",
        "Interviewer": "Focus on engineering trade-offs, scalability, and system design. Explain 'Why' we use it over alternatives."
    }
    
    current_level_instr = level_instructions.get(level, "")

    if mode == "shorts":
        return f"""
        {SYSTEM_CONTEXT}

        Create a 60-second YouTube Short script about the AI/ML technical concept: {context}
        Target Audience Technical Level: {level}
        Specific Level Instruction: {current_level_instr}
        
        Requirements:
        - Hook: Grabs attention of AI engineers or students
        - Simple Definition: Clear and technically accurate (specifically define the acronym if applicable)
        - Key Takeaway: Why this matters in an AI/ML pipeline or production environment
        
        Structure:
        - [Hook]
        - [Simple Definition]
        - [Key Takeaway]
        """
    else:
        return f"""
        {SYSTEM_CONTEXT}

        Create a detailed long-form video script for an AI/ML walkthrough.
        Context/Topic: {context}
        Technical Level: {level}
        
        Include:
        - [Introduction]: High-level purpose
        - [Deep Dive]: Technical implementation details
        - [Summary]: Final thoughts and use cases
        """
