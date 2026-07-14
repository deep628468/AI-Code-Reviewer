import re


def check_security(code):

    issues = []


    # ----------------------------
    # Hardcoded Password Detection
    # ----------------------------

    password_pattern = r"(password|passwd|pwd)\s*=\s*[\"'].*?[\"']"


    password_matches = re.findall(
        password_pattern,
        code,
        re.IGNORECASE
    )


    for match in password_matches:

        issues.append({

            "severity": "High",

            "problem": "Hardcoded password detected",

            "reason": (
                "Sensitive information is stored directly "
                "inside the source code."
            ),

            "solution": (
                "Use environment variables or a secure "
                "secret management system."
            )

        })



    # ----------------------------
    # API Key Detection
    # ----------------------------

    api_pattern = r"(api_key|apikey|secret_key)\s*=\s*[\"'].*?[\"']"


    api_matches = re.findall(
        api_pattern,
        code,
        re.IGNORECASE
    )


    for match in api_matches:

        issues.append({

            "severity": "High",

            "problem": "Possible API key exposure",

            "reason": (
                "API credentials should not be stored "
                "directly in source code."
            ),

            "solution": (
                "Store API keys in .env files."
            )

        })



    # ----------------------------
    # Dangerous eval Detection
    # ----------------------------

    if "eval(" in code:


        issues.append({

            "severity": "Critical",

            "problem": "Dangerous eval() usage",

            "reason": (
                "eval() can execute arbitrary code "
                "and create security vulnerabilities."
            ),

            "solution": (
                "Avoid eval(). Use safer alternatives."
            )

        })



    # ----------------------------
    # SQL Injection Detection
    # ----------------------------

    sql_pattern = r"(SELECT|INSERT|UPDATE|DELETE).*\+.*"


    if re.search(
        sql_pattern,
        code,
        re.IGNORECASE
    ):


        issues.append({

            "severity": "High",

            "problem": "Possible SQL Injection",

            "reason": (
                "Building SQL queries using string "
                "concatenation is unsafe."
            ),

            "solution": (
                "Use parameterized queries."
            )

        })



    return issues