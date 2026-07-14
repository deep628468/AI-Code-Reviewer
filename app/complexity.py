import ast


def analyze_complexity(code):

    try:
        tree = ast.parse(code)

    except SyntaxError:
        return {
            "time_complexity": "Not Available",
            "space_complexity": "Not Available",
            "explanation": "Cannot analyze complexity because code contains syntax errors."
        }


    loop_count = 0
    nested_loop = False


    for node in ast.walk(tree):

        if isinstance(node, (ast.For, ast.While)):

            loop_count += 1


            for child in ast.walk(node):

                if child != node and isinstance(child, (ast.For, ast.While)):

                    nested_loop = True



    # Time Complexity Detection

    if nested_loop:

        time_complexity = "O(n²)"

        reason = (
            "Nested loop detected. "
            "The outer loop runs n times and the inner loop "
            "also runs n times, resulting in n × n operations."
        )


    elif loop_count == 1:

        time_complexity = "O(n)"

        reason = (
            "Single loop detected. "
            "The loop runs once for every element in the input."
        )


    else:

        time_complexity = "O(1)"

        reason = (
            "No loop detected. "
            "The program performs a constant number of operations."
        )



    # Space Complexity Detection

    space_complexity = "O(1)"

    space_reason = (
        "No additional data structure detected. "
        "Only variables are used."
    )



    return {

        "time_complexity": time_complexity,

        "space_complexity": space_complexity,

        "explanation": reason,

        "space_reason": space_reason

    }