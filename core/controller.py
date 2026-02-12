import hashlib
import os
from core.code_explainer import explain_code
from core.diagrammer import repo_architecture_diagram, generate_concept_diagram
from core.exporter import export_markdown, export_teleprompter
from ingest.github_loader import load_github_repo, cleanup_repo
from ingest.file_parser import read_files
from rag.chunker import chunk_documents
from rag.retriever import build_vectorstore
from core.validator import Validator
from config import MAX_FILES_LONG, MAX_FILES_SHORT

validator = Validator()

def get_repo_id(repo_url):
    return hashlib.md5(repo_url.encode()).hexdigest()

def run_shorts(topic_or_url, level):
    print(f"[*] Starting SHORTS mode (Level: {level}) for: {topic_or_url}")
    
    context = ""
    is_repo = topic_or_url.startswith("http")

    if is_repo:
        print(f"[*] Cloning repository from {topic_or_url}...")
        repo_path = load_github_repo(topic_or_url)
        try:
            print(f"[+] Repo cloned to {repo_path}")
            files = read_files(repo_path, max_files=MAX_FILES_SHORT)
            print(f"[+] Read {len(files)} files for context.")
            context = "\n\n".join([f"File: {f['path']}\n{f['content']}" for f in files])
        finally:
            cleanup_repo(repo_path)
    else:
        print("[*] Using direct topic input.")
        context = topic_or_url

    from core.explainer import explain
    summary = explain(context, mode="shorts", level=level)

    # Hallucination Check for Repos
    if is_repo:
        hallucinations = validator.verify_grounding(summary, context)
        if hallucinations:
            print(f"[!] Warning: Possible hallucinations detected. Appending notes.")
            summary += "\n\n> [!WARNING]\n> Some parts of this script may contain inferred details not explicitly found in the source code."

    print("[*] Generating conceptual diagram...")
    diagram = generate_concept_diagram(context if not is_repo else topic_or_url)

    print("[+] Shorts generation complete.")
    return {
        "explanation": summary,
        "diagram": diagram,
        "markdown": export_markdown("Short_Explanation", summary),
        "teleprompter": export_teleprompter("Short_Explanation", summary)
    }

def run_long_video(repo_url, level):
    print(f"[*] Starting LONG VIDEO mode (Level: {level}) for: {repo_url}")
    repo_id = get_repo_id(repo_url)
    repo_path = load_github_repo(repo_url)

    try:
        files = read_files(repo_path, max_files=MAX_FILES_LONG)
        print(f"[+] Total files parsed: {len(files)}")

        # Build RAG
        chunks = chunk_documents(files)
        build_vectorstore(chunks, repo_id)

        explanations = []
        print("[*] Analyzing code structure and generating explanations...")
        
        full_repo_context = "\n\n".join([f"File: {f['path']}\n{f['content']}" for f in files])

        for i, f in enumerate(files):
            if f["path"].endswith(".py"):
                print(f"    ({i+1}/{len(files)}) Processing: {f['path']}")
                exp = explain_code(f, level, repo_id)
                if exp:
                    explanations.append(exp)

        architecture = repo_architecture_diagram(files)
        full_content = "\n\n".join(explanations)

        # Hallucination Check
        hallucinations = validator.verify_grounding(full_content, full_repo_context)
        if hallucinations:
            print(f"[!] Warning: Possible hallucinations detected in long video.")
            full_content = "> [!CAUTION]\n> Hallucinations detected: " + hallucinations + "\n\n" + full_content

        print("[*] Creating architecture diagram...")
        md = export_markdown("Project_Explanation", full_content)
        tp = export_teleprompter("Project_Explanation", full_content)

        print("[+] Long video analysis complete.")
        return {
            "explanation": full_content,
            "diagram": architecture,
            "markdown": md,
            "teleprompter": tp
        }

    finally:
        cleanup_repo(repo_path)
