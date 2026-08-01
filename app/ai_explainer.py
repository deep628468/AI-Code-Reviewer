import os
from dotenv import load_dotenv
from groq import Groq
from groq import APIConnectionError, APIStatusError, RateLimitError

MODEL_NAME = "llama-3.3-70b-versatile"

# =====================================
# Load Environment Variables
# =====================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=API_KEY)

# =====================================
# Explain Single Issue
# =====================================

def explain_issue(issue):

    prompt = f"""
You are an expert Python code reviewer.

Analyze this issue.

File:
{issue['file']}

Line:
{issue['line']}

Column:
{issue['column']}

Severity:
{issue['severity']}

Issue:
{issue['message']}

Respond in this format only:

Problem:
...

Reason:
...

Solution:
...

Keep the response under 100 words.
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Python code reviewer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            timeout=30
        )

        answer = response.choices[0].message.content.strip()

        return {
            "explanation": answer,
            "suggestion": answer
        }

    except RateLimitError:
        return {
            "explanation": "⚠ Groq API rate limit exceeded.",
            "suggestion": "Try again later."
        }

    except APIConnectionError as e:
      
        return {
            "explanation": "⚠ Unable to connect to Groq.",
            "suggestion": str(e)
        }

    except APIStatusError as e:
        return {
            "explanation": f"⚠ API Error {e.status_code}",
            "suggestion": str(e)
        }

    except Exception as e:
    
        return {
            "explanation": f"⚠ {e}",
            "suggestion": str(e)
        }

# =====================================
# AI Code Review
# =====================================

def review_code(code):

    prompt = f"""
You are an expert Python code reviewer.

Review the following Python code.

Mention:

1. Bugs
2. Code quality
3. Performance
4. Best practices
5. Suggestions

Python Code:

{code}
"""
    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Python reviewer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            timeout=60
        )

        return response.choices[0].message.content.strip()

    except RateLimitError:
        return "⚠ Groq API rate limit exceeded."

    except APIConnectionError as e:
       
        return f"⚠ Connection failed.\n\n{e}"

    except APIStatusError as e:
        return f"⚠ API Error {e.status_code}"

    except Exception as e:
       
        return f"⚠ Unexpected Error:\n{e}"


# =====================================
# AI Code Fix
# =====================================

def fix_code(code):

    prompt = f"""
You are an expert Python developer.

Correct the following Python code.

Fix:

- Syntax errors
- Runtime errors
- Logical errors
- Formatting
- PEP8 issues

Return ONLY valid Python code.

Do NOT include:

- Markdown
- Triple backticks
- ```python
- Explanations
- Notes
- Headings
Return ONLY corrected Python code.

Python Code:

{code}
"""
    try:
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Python developer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            timeout=60
        )

        fixed = response.choices[0].message.content.strip()

        # return fixed
    
        #     fixed = response.choices[0].message.content.strip()

        # Remove Markdown code fences if present
        if fixed.startswith("```python"):
            fixed = fixed.replace("```python", "", 1)

        if fixed.startswith("```"):
            fixed = fixed.replace("```", "", 1)

        if fixed.endswith("```"):
            fixed = fixed[:-3]

        return fixed.strip()
    
         

    except RateLimitError:
        return "⚠ Groq API rate limit exceeded."

    except APIConnectionError as e:
      
        return {
            "explanation": f"⚠ {e}",
            "suggestion": str(e)
        }

    except APIStatusError as e:
        return f"⚠ API Error {e.status_code}"

    except Exception as e:
      
        return f"⚠ Unexpected Error:\n{e}"