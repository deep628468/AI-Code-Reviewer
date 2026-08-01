import ast
import subprocess

from utils import remove_duplicates

def analyze_code(code):

    functions = []
    loops = [] 
    classes = []
    imports = []
    variables = []

    lines = len(code.strip().split("\n"))


    try:
        tree = ast.parse(code)

    except SyntaxError as e:

        return (
            [],
            [],
            [],
            [],
            [],
            lines,
            f"Syntax Error: {e}"
        )


    for node in ast.walk(tree):


        # Detect functions
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)


        # Detect loops
        if isinstance(node, ast.For):
            loops.append("For loop")


        if isinstance(node, ast.While):
            loops.append("While loop")


        # Detect classes
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)

        # Detect imports
        if isinstance(node, ast.Import):

            for name in node.names:
                imports.append(name.name)

        if isinstance(node, ast.ImportFrom):
            
            if node.module:
                imports.append(node.module)

        # Detect variables
        if isinstance(node, ast.Assign):

            for target in node.targets:

                if isinstance(target, ast.Name):
                    variables.append(target.id)



    return (
        remove_duplicates(functions),
        remove_duplicates(loops),
        remove_duplicates(classes),
        remove_duplicates(imports),
        remove_duplicates(variables),
        lines,
        None
    )



def run_flake8(file_path):

    result = subprocess.run(
        ["flake8", file_path],
        capture_output=True,
        text=True
    )


    issues = []


    for line in result.stdout.splitlines():
        
        parts = line.split(":", 3)

        if len(parts) != 4:
            continue

        file, line_no, column, message = line.split(":", 3)

        code = message.strip()


        if code.startswith("F"):
            severity = "High"

        elif code.startswith("E"):
            severity = "Medium"

        else:
            severity = "Low"


        issues.append(
            {
                "file": file,
                "line": line_no,
                "column": column,
                "severity": severity,
                "message": code
            }
        )


    return issues