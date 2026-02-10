def repo_architecture_diagram(files):
    modules = set()

    for f in files:
        parts = f["path"].split("\\")
        if "src" in parts:
            modules.add(parts[parts.index("src")+1])

    diagram = "graph TD\n"
    diagram += "User --> UI\n"
    diagram += "UI --> Controller\n"

    for m in modules:
        diagram += f"Controller --> {m}\n"

    diagram += "Controller --> LLM\n"
    diagram += "LLM --> Output\n"

    return diagram
