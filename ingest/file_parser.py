import os
from ingest.code_analyzer import analyze_python_code

SUPPORTED_EXT = (".py", ".md", ".txt")

def read_files(repo_path, max_files=None):
    files = []
    count = 0


    for root, _, filenames in os.walk(repo_path):
        for f in filenames:
            if f.endswith(SUPPORTED_EXT):
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()

                analysis = None
                if f.endswith(".py"):
                    analysis = analyze_python_code(content)

                files.append({
                    "path": path,
                    "content": content,
                    "analysis": analysis
                })
                count += 1
                if max_files and count >= max_files:
                    return files
    return files
