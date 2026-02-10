import ast

def analyze_python_code(code: str):
    tree = ast.parse(code)
    functions = []
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "lineno": node.lineno
            })

        elif isinstance(node, ast.ClassDef):
            methods = [
                n.name for n in node.body
                if isinstance(n, ast.FunctionDef)
            ]
            classes.append({
                "name": node.name,
                "methods": methods,
                "lineno": node.lineno
            })

    return {
        "functions": functions,
        "classes": classes
    }
