from core.planner import build_code_prompt
from models_code.llm_manager import llm
from config import MAX_CONTEXT_CHARS
from rag.retriever import query_vectorstore

def truncate_text(text):
    return text[:MAX_CONTEXT_CHARS] if text else ""

def extract_basic_structure(content):
    """
    Lightweight structure extraction (no heavy AST needed).
    Safe for production.
    """
    functions = []
    classes = []

    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("def "):
            try:
                functions.append(line.split("(")[0].replace("def ", ""))
            except: pass
        elif line.startswith("class "):
            try:
                classes.append(line.split("(")[0].replace("class ", "").split(":")[0])
            except: pass

    return {
        "functions": functions,
        "classes": classes
    }

def explain_code(file_data, level, repo_id):
    """
    Generates a grounded explanation for a single code file.
    """
    # Retrieve RAG context (semantic neighbors)
    context = query_vectorstore(
        f"Explain file {file_data['path']}",
        repo_id
    )
    context = truncate_text(context)

    # Use existing structure or extract on the fly
    structure = file_data.get("structure", extract_basic_structure(file_data["content"]))

    # Build prompt with RAW code to ensure maximum groundedness
    prompt = build_code_prompt(
        file_data["path"],
        file_data["content"],
        structure,
        level,
        context
    )

    # Generate using code-specialized model
    return llm.generate(prompt, mode="code")
