import os

def repo_architecture_diagram(files):
    modules = set()

    for f in files:
        parts = f["path"].replace("\\", "/").split("/")
        if len(parts) > 1:
            modules.add(parts[0])

    diagram = "graph TD\n"
    diagram += "User[User] --> UI[Streamlit UI]\n"
    diagram += "UI --> Controller\n"

    for m in modules:
        safe_name = m.replace("-", "_")
        diagram += f"Controller --> {safe_name}[{m}]\n"

    diagram += "Controller --> RAG\n"
    diagram += "Controller --> LLM\n"
    diagram += "LLM --> Output\n"

    return diagram


def generate_concept_diagram(context: str):
    """
    Deterministic conceptual diagrams for common AI terms.
    Prevents hallucinated Mermaid syntax.
    """

    context = context.lower()

    if "rag" in context:
        return """graph TD
    A[User Query] --> B[Retriever]
    B --> C[Vector Database]
    C --> B
    B --> D[Relevant Chunks]
    D --> E[LLM]
    E --> F[Final Answer]
"""

    if "fine tuning" in context or "fine-tuning" in context:
        return """graph TD
    A[Pretrained Model] --> B[Task-Specific Dataset]
    B --> C[Fine-Tuning Process]
    C --> D[Updated Weights]
    D --> E[Specialized Model]
"""

    # fallback generic AI diagram
    return """graph TD
    A[Input] --> B[Processing]
    B --> C[Model]
    C --> D[Output]
"""
