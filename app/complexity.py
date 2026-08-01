import ast


# ==========================
# Complexity Analyzer
# ==========================

def analyze_complexity(code):

    try:

        tree = ast.parse(code)

    except SyntaxError as e:

        return {
            "error": f"Syntax Error: {e}"
        }


    loops = 0
    nested_loops = 0
    functions = 0
    
    space_complexity = "O(1)"


    for node in ast.walk(tree):

        # Count functions
        if isinstance(node, ast.FunctionDef):
            functions += 1
            
            
        # Detect additional memory usage

        if isinstance(
            node,
            (
                ast.List,
                ast.Dict,
                ast.Set,
                ast.ListComp,
                ast.DictComp,
                ast.SetComp
            )
        ):
            space_complexity = "O(n)"


        # Count loops
        if isinstance(node, (ast.For, ast.While)):

            loops += 1


            # Check nested loops
            for child in ast.walk(node):

                if child != node and isinstance(
                    child,
                    (ast.For, ast.While)
                ):
                    nested_loops += 1



    # Estimate complexity

    if nested_loops >= 1:

        complexity = "O(n²)"

    elif loops > 0:

        complexity = "O(n)"

    else:

        complexity = "O(1)"



    return {

        "Functions": functions,

        "Loops": loops,

        "Nested Loops": nested_loops,

        "Estimated Time Complexity": complexity,
        
        "Estimated Space Complexity": space_complexity

    }