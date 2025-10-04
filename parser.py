import ast
from typing import Set, Dict, Any


def _extract_calls(node: ast.AST) -> Set[str]:
    calls = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            func = n.func
            if isinstance(func, ast.Name):
                calls.add(func.id)
            elif isinstance(func, ast.Attribute):
                # e.g., self.foo() or module.func()
                calls.add(func.attr)
    return calls


def parse_python_code(code: str) -> Dict[str, Any]:
    """
    Parse Python source and return:
    {
      "functions": { fname: {"name": fname, "calls": [..]} },
      "classes": { cname: {"name": cname, "methods": [{"name": m, "calls": [...]}, ...]} }
    }
    """
    tree = ast.parse(code)
    functions = {}
    classes = {}

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            calls = sorted(list(_extract_calls(node)))
            functions[node.name] = {'name': node.name, 'calls': calls}
        elif isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    calls = sorted(list(_extract_calls(item)))
                    methods.append({'name': item.name, 'calls': calls})
            classes[node.name] = {'name': node.name, 'methods': methods}

    return {'functions': functions, 'classes': classes}
