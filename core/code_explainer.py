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
            functions.append(line.split("(")[0].replace("def ", ""))
        elif line.startswith("class "):
            classes.append(line.split("(")[0].replace("class ", ""))

    return {
        "functions": functions,
        "classes": classes
    }

def explain_code(file_data, level, repo_id):

    # Retrieve RAG context
    context = query_vectorstore(
        f"Explain file {file_data['path']}",
        repo_id
    )

    context = truncate_text(context)

    # Safe structure extraction
    if "structure" in file_data:
        structure = file_data["structure"]
    else:
        structure = extract_basic_structure(file_data["content"])

    # Build prompt
    prompt = build_code_prompt(
        file_data["path"],
        file_data["content"],
        structure,
        level,
        context
    )

    # Generate
    return llm.generate(prompt, mode="code")
