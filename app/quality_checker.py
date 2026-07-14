import subprocess
from pylint.lint import Run
from pylint.reporters.text import TextReporter
from io import StringIO


def run_pylint(file_path):

    output = StringIO()

    reporter = TextReporter(output)

    Run(
        [
            file_path
        ],
        reporter=reporter,
        exit=False
    )

    return output.getvalue()



def run_flake8(file_path):

    result = subprocess.run(
        ["flake8", file_path],
        capture_output=True,
        text=True
    )

    return result.stdout



def calculate_score(issues):

    score = 100

    for issue in issues:

        if " E" in issue or " F" in issue:
            score -= 5

        elif " W" in issue:
            score -= 2


    if score < 0:
        score = 0

    return score



def format_quality_report(flake8_report):

    if not flake8_report.strip():

        return {
            "score": 100,
            "total_issues": 0,
            "report": "No code quality issues found."
        }


    issues = flake8_report.splitlines()


    score = calculate_score(issues)


    formatted = f"""
🔍 Code Quality Report

Quality Score: {score}/100

Total Issues Found: {len(issues)}


Issues:

"""


    for issue in issues:

        formatted += f"• {issue}\n"



    return {
        "score": score,
        "total_issues": len(issues),
        "report": formatted
    }



def check_quality(file_path):

    pylint_report = run_pylint(file_path)

    flake8_report = run_flake8(file_path)


    quality_report = format_quality_report(flake8_report)



    with open("code_review_report.txt", "w") as file:

        file.write("===== PYLINT REPORT =====\n")
        file.write(pylint_report)

        file.write("\n\n===== QUALITY REPORT =====\n")
        file.write(quality_report["report"])



    return {

        "pylint": pylint_report,

        # keeping this because your ui.py already uses it
        "flake8": quality_report["report"],

        "score": quality_report["score"],

        "total_issues": quality_report["total_issues"]

    }

