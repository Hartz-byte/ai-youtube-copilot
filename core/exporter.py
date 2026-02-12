import os

OUTPUT_DIR = "outputs"

def export_markdown(title, content, subfolder=""):
    target_dir = os.path.join(OUTPUT_DIR, subfolder)
    os.makedirs(target_dir, exist_ok=True)
    
    filename = os.path.join(target_dir, f"{title.replace(' ', '_')}.md")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(content)

    return filename

def export_teleprompter(title, content, subfolder=""):
    target_dir = os.path.join(OUTPUT_DIR, subfolder)
    os.makedirs(target_dir, exist_ok=True)
    
    filename = os.path.join(target_dir, f"{title.replace(' ', '_')}_teleprompter.txt")

    # Filter out the [!TIP] block for the teleprompter to keep it script-only
    script_only = content.split("> [!TIP]")[0].strip()

    lines = script_only.split("\n")
    slow_lines = "\n\n".join(lines)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(slow_lines)

    return filename
