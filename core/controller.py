from core.code_explainer import explain_code
from core.diagrammer import repo_architecture_diagram
from core.exporter import export_markdown, export_teleprompter
from ingest.github_loader import load_github_repo
from ingest.file_parser import read_files


def run_shorts(topic_or_url, level):
    """
    SHORTS MODE:
    - High-level explanation
    - Key files only (if repo) or general (if topic)
    - Concise output
    """
    
    if topic_or_url.startswith("http"):
        repo_path = load_github_repo(topic_or_url)
        files = read_files(repo_path, max_files=5)
        context = "\n\n".join([f["content"] for f in files])
    else:
        context = topic_or_url

    from core.explainer import explain
    summary = explain(context, mode="shorts", level=level)

    return {
        "explanation": summary,
        "diagram": None,
        "markdown": export_markdown("Short_Explanation", summary),
        "teleprompter": export_teleprompter("Short_Explanation", summary)
    }


def run_long_video(repo_url, level):
    """
    LONG VIDEO MODE:
    - Full repo scan
    - Architecture diagram
    - Deep explanations
    """

    repo_path = load_github_repo(repo_url)
    files = read_files(repo_path)

    explanations = []
    for f in files:
        code_exp = explain_code(f)
        if code_exp:
            explanations.append(code_exp)

    architecture = repo_architecture_diagram(files)
    full_content = "\n\n".join(explanations)

    return {
        "explanation": full_content,
        "diagram": architecture,
        "markdown": export_markdown("Project_Explanation", full_content),
        "teleprompter": export_teleprompter("Project_Explanation", full_content)
    }
