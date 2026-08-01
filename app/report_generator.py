def generate_report(
    functions,
    classes,
    loops,
    imports,
    variables,
    lines,
    complexity,
    quality_issues,
    security_issues,
    ai_review
):

    report = f"""
================================
AI CODE REVIEW REPORT
================================


📌 CODE ANALYSIS

Functions:
{len(functions)}

Classes:
{len(classes)}

Loops:
{len(loops)}

Imports:
{len(imports)}

Variables:
{len(variables)}

Lines of Code:
{lines}


⚡ COMPLEXITY ANALYSIS

Time Complexity:
{complexity['time_complexity']}

Explanation:
{complexity['explanation']}


Space Complexity:
{complexity['space_complexity']}

Reason:
{complexity['space_reason']}



🔍 QUALITY REPORT

"""


    if quality_issues:

        for issue in quality_issues:

            report += (
                f"\n{issue['severity']} : "
                f"{issue['message']}"
            )

    else:

        report += "\nNo quality issues found"



    report += """


🛡 SECURITY REPORT

"""


    if security_issues:

        for issue in security_issues:

            report += f"""

Severity:
{issue['severity']}

Problem:
{issue['problem']}

Reason:
{issue['reason']}

Solution:
{issue['solution']}

"""

    else:

        report += "\nNo security issues detected"



    report += f"""


🤖 AI REVIEW

{ai_review}

================================
END OF REPORT
================================

"""
    return report