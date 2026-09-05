import os
from dotenv import load_dotenv
from groq import Groq
from groq import APIConnectionError, APIStatusError, RateLimitError

MODEL_NAME =  "openai/gpt-oss-120b" 

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

Python Code:

Provide a concise professional review covering:

1. Bugs
2. Code quality
3. Performance
4. Best practices
5. Suggestions



Rules:
- Keep the entire review under 120 words.
- Use short, professional bullet points.
- Do not repeat or rewrite the submitted code.
- Focus on actual bugs, risks, and meaningful improvements.
- Do not suggest unnecessary changes for simple code.
- Do not recommend logging, error handling, type hints, or documentation unless they are genuinely relevant.
- Do not explain basic Python concepts.
- If the code is already correct, clearly state that and mention only 1–2 useful improvements.

{code}
"""
    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,
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

    # except APIStatusError as e:
    #     return f"⚠ API Error {e.status_code}"

    except APIStatusError as e:
        return f"⚠ API Error {e.status_code}\n\nDetails: {e}"
    
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
            model=MODEL_NAME,
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
        return f"⚠ Connection failed.\n\n{e}"

    # except APIStatusError as e:
    #     return f"⚠ API Error {e.status_code}"
    
    except APIStatusError as e:
        return f"⚠ API Error {e.status_code}\n\nDetails: {e}"

    except Exception as e:
      
        return f"⚠ Unexpected Error:\n{e}"