from core.code_explainer import explain_code
from core.diagrammer import repo_architecture_diagram
from core.exporter import export_markdown, export_teleprompter
from ingest.github_loader import load_github_repo
from ingest.file_parser import read_files
import hashlib
from core.code_explainer import explain_code
from core.diagrammer import repo_architecture_diagram
from core.exporter import export_markdown, export_teleprompter
from ingest.github_loader import load_github_repo, cleanup_repo
from ingest.file_parser import read_files
from rag.chunker import chunk_documents
from rag.retriever import build_vectorstore
from config import MAX_FILES_LONG, MAX_FILES_SHORT

def run_shorts(topic_or_url, level):
    # ... previous docstring ...
    print(f"[*] Starting SHORTS mode (Level: {level}) for: {topic_or_url}")
    
    if topic_or_url.startswith("http"):
        print(f"[*] Cloning repository from {topic_or_url}...")
        repo_path = load_github_repo(topic_or_url)
        print(f"[+] Repo cloned to {repo_path}")
        files = read_files(repo_path, max_files=5)
        print(f"[+] Read {len(files)} files for context.")
        context = "\n\n".join([f["content"] for f in files])
    else:
        print("[*] Using direct topic input.")
        context = topic_or_url

    from core.explainer import explain
    summary = explain(context, mode="shorts", level=level)

    from core.diagrammer import generate_concept_diagram
    print("[*] Generating conceptual diagram...")
    diagram = generate_concept_diagram(context)

    print("[+] Shorts generation complete.")
    return {
        "explanation": summary,
        "diagram": diagram,
        "markdown": export_markdown("Short_Explanation", summary),
        "teleprompter": export_teleprompter("Short_Explanation", summary)
    }


def get_repo_id(repo_url):
    return hashlib.md5(repo_url.encode()).hexdigest()

def run_long_video(repo_url, level):
    repo_id = get_repo_id(repo_url)
    repo_path = load_github_repo(repo_url)

    try:
        files = read_files(repo_path, max_files=MAX_FILES_LONG)

        # Build RAG
        chunks = chunk_documents(files)
        build_vectorstore(chunks, repo_id)

        explanations = []

        for f in files:
            if f["path"].endswith(".py"):
                exp = explain_code(f, level, repo_id)
                explanations.append(exp)

        architecture = repo_architecture_diagram(files)

        full_content = "\n\n".join(explanations)

        md = export_markdown("Project_Explanation", full_content)
        tp = export_teleprompter("Project_Explanation", full_content)

        return {
            "explanation": full_content,
            "diagram": architecture,
            "markdown": md,
            "teleprompter": tp
        }

    finally:
        cleanup_repo(repo_path)
