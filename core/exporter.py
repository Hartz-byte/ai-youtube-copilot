import os
from datetime import datetime

OUTPUT_DIR = "outputs"

def export_markdown(title, content):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{OUTPUT_DIR}/{title.replace(' ', '_')}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(content)

    return filename


def export_teleprompter(title, content):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{OUTPUT_DIR}/{title.replace(' ', '_')}_teleprompter.txt"

    lines = content.split("\n")
    slow_lines = "\n\n".join(lines)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(slow_lines)

    return filename
