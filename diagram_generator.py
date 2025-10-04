import ast
import tempfile
import subprocess
import os
import base64

DOT_EXE = r"C:\Program Files\Graphviz\bin\dot.exe"  # Adjust if installed elsewhere

class CallGraphVisitor(ast.NodeVisitor):
    def __init__(self):
        self.calls = []
        self.current_func = None

    def visit_FunctionDef(self, node):
        prev_func = self.current_func
        self.current_func = node.name
        self.generic_visit(node)
        self.current_func = prev_func

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        else:
            func_name = "unknown"

        if self.current_func:
            self.calls.append((self.current_func, func_name))
        self.generic_visit(node)

def generate_diagram(code_text: str) -> str:
    try:
        tree = ast.parse(code_text)
        visitor = CallGraphVisitor()
        visitor.visit(tree)

        dot_code = "digraph G {\n"
        dot_code += 'rankdir=LR;\nnode [shape=box, style=filled, color="#4a90e2", fontname="Arial", fontsize=12, fillcolor="#eaf4ff"];\n'

        seen = set()
        for caller, callee in visitor.calls:
            dot_code += f'"{caller}" -> "{callee}";\n'
            seen.add(caller)
            seen.add(callee)
        for node in seen:
            dot_code += f'"{node}";\n'
        dot_code += "}"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".dot") as f:
            f.write(dot_code.encode("utf-8"))
            dot_path = f.name

        png_path = dot_path.replace(".dot", ".png")
        subprocess.run([DOT_EXE, "-Tpng", dot_path, "-o", png_path], check=True)

        with open(png_path, "rb") as f:
            img_bytes = f.read()
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        os.remove(dot_path)
        os.remove(png_path)

        return img_base64
    except Exception as e:
        return None
